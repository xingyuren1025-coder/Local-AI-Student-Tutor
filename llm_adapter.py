import torch
import time
import psutil
import os
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
from config_manager import MODEL_NAME


@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype="auto",
        device_map="auto"
    )
    return model, tokenizer


def get_resource_usage():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info().rss / (1024 ** 2)  # MB
    cpu_usage = psutil.cpu_percent(interval=None)
    return mem_info, cpu_usage


def run_inference(user_input, system_instruction, messages, model, tokenizer):
    # 开始监控资源与时间
    start_mem, _ = get_resource_usage()
    start_time = time.perf_counter()

    # --- 步骤 1: 英文推理 ---
    strict_english_prompt = f"Answer the following question in ENGLISH ONLY. Question: {user_input}"
    qwen_messages = [{"role": "system", "content": system_instruction}]

    # 保持对话上下文
    for msg in messages[-4:]:
        qwen_messages.append({"role": msg["role"], "content": msg["content"]})
    qwen_messages.append({"role": "user", "content": strict_english_prompt})

    text_input = tokenizer.apply_chat_template(qwen_messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text_input], return_tensors="pt").to(model.device)

    with torch.no_grad():
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=450,
            temperature=0.3,
            do_sample=True
        )

    eng_res = tokenizer.decode(generated_ids[0][len(model_inputs.input_ids[0]):], skip_special_tokens=True).strip()

    # --- 步骤 2: 中文翻译 ---
    translate_prompt = [
        {"role": "system", "content": "You are a professional Chinese translator."},
        {"role": "user", "content": f"Translate this into Chinese: {eng_res}"}
    ]
    trans_input = tokenizer.apply_chat_template(translate_prompt, tokenize=False, add_generation_prompt=True)
    trans_inputs = tokenizer([trans_input], return_tensors="pt").to(model.device)

    with torch.no_grad():
        trans_gen_ids = model.generate(**trans_inputs, max_new_tokens=500, temperature=0.1)

    chn_res = tokenizer.decode(trans_gen_ids[0][len(trans_inputs.input_ids[0]):], skip_special_tokens=True).strip()

    # --- 结束监控 ---
    # 修复点：定义 end_time 并获取最终资源数据
    end_time = time.perf_counter()
    end_mem, cpu_perc = get_resource_usage()

    # 计算最终性能指标
    latency = round(end_time - start_time, 2)
    mem_used = round(end_mem, 2)

    return eng_res, chn_res, latency, mem_used, cpu_perc