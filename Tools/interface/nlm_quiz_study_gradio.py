import gradio as gr
import os
import sys
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'user_obs'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'local_llm'))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BASE_DOCS_DIR

# --- Utility functions ---
def get_courses():
    docs_dir = BASE_DOCS_DIR or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'Docs')
    if not os.path.exists(docs_dir):
        return []
    return [d for d in os.listdir(docs_dir) if os.path.isdir(os.path.join(docs_dir, d))]

def parse_quiz_md(quiz_path):
    with open(quiz_path, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = re.compile(
        r'(\d+)\.\s*(.*?)\nA\)\s*(.*?)\nB\)\s*(.*?)\nC\)\s*(.*?)\nD\)\s*(.*?)\nAnswer:\s*([A-D])\)?',
        re.DOTALL
    )
    parsed = []
    for match in pattern.finditer(content):
        question_text = match.group(2).strip()
        options = [
            f"A) {match.group(3).strip()}",
            f"B) {match.group(4).strip()}",
            f"C) {match.group(5).strip()}",
            f"D) {match.group(6).strip()}"
        ]
        answer = match.group(7)
        parsed.append((question_text, options, answer))
    return parsed

def get_course_content(course_code):
    base = os.path.join(BASE_DOCS_DIR, course_code)
    content = {}
    # Notes PDFs
    notes_dir = os.path.join(base, f"{course_code}_notes")
    content['PDF Notes'] = [f for f in os.listdir(notes_dir)] if os.path.exists(notes_dir) else []
    # AI Summaries
    ai_sum_dir = os.path.join(base, f"{course_code}_ai_summaries")
    content['AI Summaries'] = [f for f in os.listdir(ai_sum_dir)] if os.path.exists(ai_sum_dir) else []
    # Expected Q&A
    exp_qa_dir = os.path.join(base, f"{course_code}_exp_ques")
    content['Expected Q&A'] = [f for f in os.listdir(exp_qa_dir)] if os.path.exists(exp_qa_dir) else []
    # Markdown
    md_dir = os.path.join(base, f"{course_code}_md")
    content['Markdown'] = [f for f in os.listdir(md_dir)] if os.path.exists(md_dir) else []
    return content

# --- Gradio pipeline logic ---
def quiz_interface(course_code, user_name):
    quiz_path = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_md", "general_quiz.md")
    if not os.path.exists(quiz_path):
        return gr.update(visible=False), f"Quiz file not found for course: {course_code}", None, None
    questions = parse_quiz_md(quiz_path)[:10]
    session = {'questions': questions, 'user': user_name, 'course': course_code, 'answers': []}
    return gr.update(visible=True), '', session, 0

def show_question(session, idx):
    questions = session['questions']
    if idx >= len(questions):
        # 8 outputs: quiz_box, q_text, optA, optB, optC, optD, feedback, next_btn
        return gr.update(visible=False), '', '', '', '', '', '', '', True
    q, opts, _ = questions[idx]
    # 8 outputs: quiz_box, q_text, optA, optB, optC, optD, feedback, next_btn
    return gr.update(visible=True), f"Q{idx+1}: {q}", opts[0], opts[1], opts[2], opts[3], '', '', False

def record_answer(session, idx, user_ans):
    questions = session['questions']
    q, opts, ans = questions[idx]
    session['answers'].append({'question': q, 'options': opts, 'correct': ans, 'user': user_ans})
    idx += 1
    if idx >= len(questions):
        return session, idx, True
    return session, idx, False

def analyze_results(session):
    wrong = []
    for a in session['answers']:
        if a['user'] != a['correct']:
            wrong.append({'question': a['question'], 'user_answer': a['user'], 'correct_answer': a['correct']})
    score = sum(1 for a in session['answers'] if a['user'] == a['correct'])
    total = len(session['answers'])
    # Save wrong answers to temp file and get recommendations
    if wrong:
        from user_obs.quiz_watchdog import record_wrong_answers
        import glob
        from local_llm.quiz_recommender_gemini import get_recommendations_from_gemini
        record_wrong_answers(wrong, username=session['user'])
        user_analysis_dir = os.path.join(os.path.dirname(__file__), "../user_obs/user_analysis")
        pattern = os.path.join(user_analysis_dir, f"{session['user']}_wrong_*.txt")
        files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
        if files:
            recs = get_recommendations_from_gemini(files[0])
        else:
            recs = "No analysis file found."
    else:
        recs = "All answers correct!"
    return f"Score: {score}/{total}\n\n{recs}"

def content_page(course_code):
    content = get_course_content(course_code)
    md = f"# Content for {course_code}\n"
    for k, v in content.items():
        md += f"\n## {k}\n"
        if v:
            for f in v:
                md += f"- {f}\n"
        else:
            md += "_None found._\n"
    return md

# --- Gradio UI ---
with gr.Blocks(theme=gr.themes.Soft(), title="NLM Quiz & Study Plan UI") as demo:
    gr.Markdown("# NLM Quiz & Study Plan\nA clean pipeline for user analysis and content access.")
    with gr.Row():
        course_list = gr.Dropdown(label="Select Course", choices=get_courses(), interactive=True)
        user_name = gr.Textbox(label="Your Name", value="default_user")
        start_btn = gr.Button("Start Quiz")
    quiz_box = gr.Group(visible=False)
    with quiz_box:
        q_text = gr.Markdown()
        with gr.Row():
            optA = gr.Button(interactive=True, elem_id="optA", scale=1)
            optB = gr.Button(interactive=True, elem_id="optB", scale=1)
        with gr.Row():
            optC = gr.Button(interactive=True, elem_id="optC", scale=1)
            optD = gr.Button(interactive=True, elem_id="optD", scale=1)
        feedback = gr.Markdown(visible=False)
        progress = gr.Markdown(visible=True)
    result_box = gr.Textbox(label="Analysis & Study Plan", visible=False, interactive=False)
    content_btn = gr.Button("Go to Course Content", visible=False)
    content_md = gr.Markdown(visible=False)

    # State
    session = gr.State()
    idx = gr.State()
    quiz_done = gr.State()
    score = gr.State()

    def start_quiz(course, user):
        quiz_path = os.path.join(BASE_DOCS_DIR, course, f"{course}_md", "general_quiz.md")
        if not os.path.exists(quiz_path):
            return gr.update(visible=False), '', '', '', '', '', '', '', 0, 0, 0, 0
        questions = parse_quiz_md(quiz_path)[:10]
        session = {'questions': questions, 'user': user, 'course': course, 'answers': [], 'score': 0}
        idx = 0
        q, opts, _ = questions[idx]
        progress_str = f"**Question {idx+1}/10** | **Score: 0**"
        return gr.update(visible=True), f"Q{idx+1}: {q}", opts[0], opts[1], opts[2], opts[3], gr.update(visible=False), progress_str, session, idx, False, 0

    def handle_option(opt, session, idx, score):
        questions = session['questions']
        q, opts, ans = questions[idx]
        correct = (opt == ans)
        session['answers'].append({'question': q, 'options': opts, 'correct': ans, 'user': opt})
        if correct:
            session['score'] = session.get('score', 0) + 1
            feedback_str = f"<span style='color:green;font-weight:bold'>Correct!</span>"
        else:
            feedback_str = f"<span style='color:red;font-weight:bold'>Incorrect. Correct answer: {ans}</span>"
        idx += 1
        if idx >= len(questions):
            # Record all answers (correct and wrong) for audit/tracking
            try:
                from user_obs.quiz_watchdog import record_quiz_answers
                # answers in session['answers'] are in the format: {'question', 'options', 'correct', 'user'}
                # Convert to expected format for record_quiz_answers
                all_answers = []
                for a in session['answers']:
                    all_answers.append({
                        'question': a['question'],
                        'user_answer': a['user'],
                        'correct_answer': a['correct']
                    })
                record_quiz_answers(all_answers, username=session.get('user', 'default_user'))
            except Exception as e:
                print(f"[Watchdog] Error recording all answers: {e}")
            analysis = analyze_results(session)
            return gr.update(visible=False), '', '', '', '', '', '', '', session, idx, True, session['score'], analysis, True, ''
        q, opts, _ = questions[idx]
        progress_str = f"**Question {idx+1}/10** | **Score: {session['score']}**"
        return gr.update(visible=True), f"Q{idx+1}: {q}", opts[0], opts[1], opts[2], opts[3], gr.update(visible=True, value=feedback_str), progress_str, session, idx, False, session['score'], '', False, ''

    start_btn.click(start_quiz, [course_list, user_name], [quiz_box, q_text, optA, optB, optC, optD, feedback, progress, session, idx, quiz_done, score])
    optA.click(lambda s, i, sc: handle_option('A', s, i, sc), [session, idx, score], [quiz_box, q_text, optA, optB, optC, optD, feedback, progress, session, idx, quiz_done, score, result_box, content_btn, content_md])
    optB.click(lambda s, i, sc: handle_option('B', s, i, sc), [session, idx, score], [quiz_box, q_text, optA, optB, optC, optD, feedback, progress, session, idx, quiz_done, score, result_box, content_btn, content_md])
    optC.click(lambda s, i, sc: handle_option('C', s, i, sc), [session, idx, score], [quiz_box, q_text, optA, optB, optC, optD, feedback, progress, session, idx, quiz_done, score, result_box, content_btn, content_md])
    optD.click(lambda s, i, sc: handle_option('D', s, i, sc), [session, idx, score], [quiz_box, q_text, optA, optB, optC, optD, feedback, progress, session, idx, quiz_done, score, result_box, content_btn, content_md])

    def show_content(course):
        return content_page(course), True
    content_btn.click(lambda s: show_content(s['course']), session, [content_md, content_md])

demo.launch()
