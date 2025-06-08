import gradio as gr
from agent_core import AgentCore

agent = AgentCore()

def respond(history, user_message):
    response = agent.decide_and_execute(user_message)
    history = history or []
    history.append((user_message, response))
    return history, ""

with gr.Blocks(theme=gr.themes.Soft(), title="NLM Agent Chatbot") as demo:
    gr.Markdown("# NLM Agent Chatbot\nChat with the autonomous agent to use all toolkit features via natural language.")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Your message")
    send_btn = gr.Button("Send")

    send_btn.click(
        respond,
        inputs=[chatbot, msg],
        outputs=[chatbot, msg]
    )

demo.launch()
