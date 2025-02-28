import gradio as gr
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

# Validate API key
if not api_key or api_key == "YOUR_GEMINI_API_KEY":
    raise ValueError("Invalid or missing API_KEY. Please set a valid API key in the .env file.")

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro')

# Load knowledge base
try:
    with open('knowledge_base.json', 'r') as f:
        knowledge_base = json.load(f)
except FileNotFoundError:
    knowledge_base = {}
    print("Warning: knowledge_base.json not found. Starting with empty knowledge base.")

# Check knowledge base for response
def get_response_from_knowledge_base(intent):
    return knowledge_base.get(intent)

# Check if input is stock market related
def is_stock_market_related(user_input):
    keywords = ["stock", "market", "invest", "share", "dividend", "ipo", "trading", "bonds", "portfolio", 
                "analysis", "broker", "fund", "etf", "capital", "bull", "bear", "volume", "chart", "price"]
    return any(keyword in user_input.lower() for keyword in keywords)

# Interact with Gemini API
def chat_with_gemini(user_input, chat_history):
    prompt = """
    You are an expert stock market tutor named Sage whose job is to educate people on the stock market.
    If the user asks anything not stock market related, politely decline.
    Otherwise, answer the question and keep your answers concise and precise.
    Note: I cannot provide live stock market prices or current updates as I don’t have real-time data access.
    """
    gemini_formatted_history = [{"role": "user", "parts": [prompt]}]
    for user_msg, bot_msg in chat_history:
        gemini_formatted_history.append({"role": "user", "parts": [user_msg]})
        gemini_formatted_history.append({"role": "model", "parts": [bot_msg]})
    gemini_formatted_history.append({"role": "user", "parts": [user_input]})
    
    try:
        response = model.generate_content(gemini_formatted_history)
        return response.text
    except Exception as e:
        return f"Error: Could not fetch response from Gemini API - {str(e)}"

# Chatbot logic
def chatbot(user_input, chat_history):
    if not user_input.strip():
        return "Please ask a question", chat_history
    if is_stock_market_related(user_input):
        response_from_kb = get_response_from_knowledge_base(user_input)
        bot_response = response_from_kb if response_from_kb else chat_with_gemini(user_input, chat_history)
    else:
        bot_response = "I can only answer questions about the stock market."
    chat_history.append((user_input, bot_response))
    return "", chat_history

# Clear chat history
def clear_history():
    return []

# Gradio interface
with gr.Blocks(title="Market Mentor") as demo:
    gr.Markdown("# Market Mentor\n### Your Guide to the Stock Market\n##### I am Sage, your stock market tutor")
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Accordion("Categories"):
                gr.Markdown("### Main\n* Basics\n* Investing\n* Analysis\n* Risk\n\n### Topics\n* What are Stocks\n* How to Trade\n* What are IPO's\n* And many more!")
        with gr.Column(scale=4):
            chatbot_state = gr.State([])
            chatbot_history = gr.Chatbot(elem_id="chat_bot")
            input_text = gr.Textbox(placeholder="Enter your question here...")
            with gr.Row():
                clear_btn = gr.Button("Clear History", variant="secondary")
                submit_btn = gr.Button("Send", variant="primary")
            clear_btn.click(clear_history, outputs=chatbot_state)
            submit_btn.click(chatbot, [input_text, chatbot_state], [input_text, chatbot_history])
            input_text.submit(chatbot, [input_text, chatbot_state], [input_text, chatbot_history])
    css = """
    #chat_bot { height: 400px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; }
    .gradio-container { background-color: #F5F5F5; }
    #chat_bot .user { background-color: #1A237E; color: white; border-radius: 10px; padding: 8px; margin-bottom: 5px; }
    #chat_bot .bot { background-color: #4DD0E1; color: black; border-radius: 10px; padding: 8px; margin-bottom: 5px; }
    .gr-button { background-color: #1A237E; color: white; font-weight: bold; }
    """
demo.launch(share=True, server_port=7860)