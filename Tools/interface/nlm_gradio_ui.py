import gradio as gr
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.agent_core import AgentCore

agent = AgentCore()

def create_folders_ui(course_code):
    try:
        from general_tools import create_course_folders
        create_course_folders.create_course_folders(course_code)
        return f"Folders created for {course_code}."
    except Exception as e:
        return str(e)

def extract_pdf_ui(course_code):
    try:
        from local_llm import extract_pdf_text
        extract_pdf_text.extract_text_from_pdfs(course_code)
        return f"PDF text extracted for {course_code}."
    except Exception as e:
        return str(e)

def clean_chunk_ui(course_code):
    try:
        from general_tools import clean_and_chunk_texts
        clean_and_chunk_texts.process_text_files(course_code)
        return f"Text cleaned and chunked for {course_code}."
    except Exception as e:
        return str(e)

def summarize_ui(course_code):
    try:
        from local_llm import summarize_chunks_with_ollama
        summarize_chunks_with_ollama.main(course_code)
        return f"Summaries generated for {course_code}."
    except Exception as e:
        return str(e)

def qa_ui(course_code):
    try:
        from local_llm import generate_expected_qa_with_ollama
        generate_expected_qa_with_ollama.main(course_code)
        return f"Expected Q&A generated for {course_code}."
    except Exception as e:
        return str(e)

def quiz_ui(course_code):
    try:
        from local_llm import generate_quizzes_with_ollama
        generate_quizzes_with_ollama.main(course_code)
        return f"Quizzes generated for {course_code}."
    except Exception as e:
        return str(e)

def combine_md_ui(course_code):
    try:
        from general_tools import combine_md_files
        combine_md_files.combine_md_summaries(course_code)
        return f"Markdown files combined for {course_code}."
    except Exception as e:
        return str(e)

def md_to_pdf_ui(course_code):
    try:
        from general_tools import md_to_pdf
        md_to_pdf.convert_md_to_pdf(course_code)
        return f"PDFs exported for {course_code}."
    except Exception as e:
        return str(e)

with gr.Blocks(theme=gr.themes.Soft(), title="NLM Toolkit UI") as demo:
    gr.Markdown("# NLM Toolkit\nMinimal, user-friendly interface for all tools.")
    with gr.Tab("Course Setup"):
        course_code = gr.Textbox(label="Course Code")
        create_btn = gr.Button("Create Folders")
        create_out = gr.Textbox(label="Output")
        create_btn.click(create_folders_ui, inputs=course_code, outputs=create_out)
    with gr.Tab("PDF Extraction"):
        course_code2 = gr.Textbox(label="Course Code")
        extract_btn = gr.Button("Extract PDF Text")
        extract_out = gr.Textbox(label="Output")
        extract_btn.click(extract_pdf_ui, inputs=course_code2, outputs=extract_out)
    with gr.Tab("Chunking"):
        course_code3 = gr.Textbox(label="Course Code")
        chunk_btn = gr.Button("Clean & Chunk Text")
        chunk_out = gr.Textbox(label="Output")
        chunk_btn.click(clean_chunk_ui, inputs=course_code3, outputs=chunk_out)
    with gr.Tab("Summarization"):
        course_code4 = gr.Textbox(label="Course Code")
        sum_btn = gr.Button("Summarize Chunks")
        sum_out = gr.Textbox(label="Output")
        sum_btn.click(summarize_ui, inputs=course_code4, outputs=sum_out)
    with gr.Tab("Q&A Generation"):
        course_code5 = gr.Textbox(label="Course Code")
        qa_btn = gr.Button("Generate Q&A")
        qa_out = gr.Textbox(label="Output")
        qa_btn.click(qa_ui, inputs=course_code5, outputs=qa_out)
    with gr.Tab("Quiz Generation"):
        course_code6 = gr.Textbox(label="Course Code")
        quiz_btn = gr.Button("Generate Quizzes")
        quiz_out = gr.Textbox(label="Output")
        quiz_btn.click(quiz_ui, inputs=course_code6, outputs=quiz_out)
    with gr.Tab("Combine Markdown"):
        course_code7 = gr.Textbox(label="Course Code")
        combine_btn = gr.Button("Combine Markdown Files")
        combine_out = gr.Textbox(label="Output")
        combine_btn.click(combine_md_ui, inputs=course_code7, outputs=combine_out)
    with gr.Tab("Export to PDF"):
        course_code8 = gr.Textbox(label="Course Code")
        pdf_btn = gr.Button("Export PDFs")
        pdf_out = gr.Textbox(label="Output")
        pdf_btn.click(md_to_pdf_ui, inputs=course_code8, outputs=pdf_out)

demo.launch()
