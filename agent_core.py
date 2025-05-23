import subprocess
import json
import logging
from agent_memory import AgentMemory

# Set up logging
logging.basicConfig(filename="agent.log", level=logging.INFO, format="%(asctime)s %(message)s")

TOOLS_DIR = "Tools/"
ALLOWED_SCRIPTS = [
    "clean_and_chunk_texts.py",
    "combine_md_files.py",
    "create_course_folders.py",
    "extract_pdf_text.py",
    # "find_pdfs_in_notes.py",
    "generate_expected_qa_with_ollama.py",
    "generate_quizzes_with_ollama.py",
    "md_to_pdf.py",
    "quiz_recommender.py",
    "quiz_watchdog.py",
    "summarize_chunks_with_ollama.py",
    "terminal_quiz_runner.py"
]

class AgentCore:
    def __init__(self):
        self.memory = AgentMemory()

    def call_ollama_llama3(self, prompt):
        # Call local Ollama Llama3 model via subprocess (API or CLI)
        # Send prompt via stdin, as in summarize_chunks_with_ollama.py
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120
        )
        if result.returncode != 0:
            logging.error(f"Ollama error: {result.stderr.decode('utf-8')}")
            return ""
        return result.stdout.decode('utf-8').strip()

    def decide_and_execute(self, user_message):
        # Retrieve relevant memory for context
        memory_results = self.memory.query_memory(user_message, n_results=3)
        # Flatten the documents list in case it contains nested lists
        documents = memory_results.get("documents", [""])
        flat_documents = []
        for doc in documents:
            if isinstance(doc, list):
                flat_documents.extend([str(d) for d in doc])
            else:
                flat_documents.append(str(doc))
        context = "\n".join(flat_documents)
        # Compose prompt for Llama3
        prompt = f"""
You are an autonomous agent. Given the user message and context, decide which script to run from the following list: {ALLOWED_SCRIPTS}.
User message: {user_message}
Relevant context: {context}
Respond ONLY with a JSON object: {{'script': <script_name>, 'args': <list of args>}}. If no script is needed, respond with {{'script': null, 'args': []}}.
"""
        decision = self.call_ollama_llama3(prompt)
        # Log the raw model output for debugging
        logging.info(f"Raw Llama3 output: {decision}")
        try:
            decision_json = json.loads(decision.replace("'", '"'))
        except Exception:
            # Try to extract JSON object from the output if extra text is present
            import re
            match = re.search(r'\{.*\}', decision, re.DOTALL)
            if match:
                try:
                    decision_json = json.loads(match.group(0).replace("'", '"'))
                except Exception as e:
                    logging.error(f"Failed to parse extracted JSON from Llama3 output: {decision}\nError: {e}")
                    return f"Agent output could not be parsed as JSON. Raw output: {decision}"
            else:
                logging.error(f"Failed to parse Llama3 output: {decision}")
                return f"Agent output could not be parsed as JSON. Raw output: {decision}"
        script = decision_json.get("script")
        args = decision_json.get("args", [])
        if script and script in ALLOWED_SCRIPTS:
            script_path = TOOLS_DIR + script
            # Security: Only allow whitelisted scripts
            try:
                result = subprocess.run([
                    "python", script_path, *args
                ], capture_output=True, text=True, timeout=120)
                output = result.stdout.strip()
                logging.info(f"Ran {script} with args {args}. Output: {output}")
            except Exception as e:
                logging.error(f"Error running {script}: {e}")
                output = f"Error running script: {e}"
        else:
            output = "No valid script selected or needed."
        # Save user message and output to memory
        self.memory.add_memory(f"User: {user_message}")
        self.memory.add_memory(f"Agent: {output}")
        return output
