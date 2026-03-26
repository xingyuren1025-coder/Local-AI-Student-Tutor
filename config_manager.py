import os

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "chatbot_logs.csv")
INSTRUCTION_FILE = os.path.join(BASE_DIR, "chatbot_instructions.txt")

# 函数 1：读取指令
def load_instructions():
    if not os.path.exists(INSTRUCTION_FILE):
        return "You are a professional academic AI tutor. Explain technical concepts clearly."
    with open(INSTRUCTION_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

# 函数 2：保存指令 (你可能漏掉了这个函数)
def save_instructions(new_text):
    with open(INSTRUCTION_FILE, "w", encoding="utf-8") as f:
        f.write(new_text)