import streamlit as st
import pandas as pd
import os
import csv
from config_manager import load_instructions, save_instructions, LOG_FILE
from data_manager import log_chat, get_excel_data
from llm_adapter import load_model, run_inference
from auth import admin_login

# 1. 页面配置
# 1. Page Configuration
st.set_page_config(page_title="AI Student Tutor", page_icon="🎓", layout="wide")
is_admin = admin_login()  # Sidebar Login function 侧边栏登录逻辑
system_instruction = load_instructions()

st.title("🎓 AI Student Tutor | AI 学生辅导助手")
st.caption("University Student Academic Support Tool | 大学生学业支持工具")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. 加载模型
# 2. Load the model
with st.spinner("Loading Local LLM..."):
    model, tokenizer = load_model()

# 3. 渲染历史对话 (双栏布局)
# 3. Render Historical Conversations (Two-Column Layout)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "translation" in message:
            # 历史记录中的性能显示
            # Performance Display
            if "latency" in message:
                st.caption(f"📊 Metrics: {message['latency']}s | RAM: {message.get('mem', 0)}MB")
            col1, col2 = st.columns(2)
            col1.markdown("**🇺🇸 English Response**\n\n" + message["content"])
            col2.markdown("**🇨🇳 中文翻译**\n\n" + message["translation"])
        else:
            st.markdown(message["content"])

# 4. 核心聊天逻辑
# 4. Core Chat Logic
if user_input := st.chat_input("Ask a technical question..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        # 获取 5 个性能与内容参数
        # Get 5 performance and content parameters
        eng_res, chn_res, latency, mem_used, cpu_perc = run_inference(
            user_input, system_instruction, st.session_state.messages, model, tokenizer
        )

        # 实时显示性能测量
        # Performance Measurement
        st.caption(f"⚡ Performance Metrics: Latency: {latency}s | RAM: {mem_used}MB | CPU: {cpu_perc}%")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🇺🇸 English Response**\n\n" + eng_res)
        with col2:
            st.markdown("**🇨🇳 中文翻译**\n\n" + chn_res)

    # 5. 状态存储与日志记录
    # 5. State Storage and Logging
    st.session_state.messages.append({
        "role": "assistant",
        "content": eng_res,
        "translation": chn_res,
        "latency": latency,
        "mem": mem_used
    })

    # 合并性能数据、英文和中文存入日志，确保导出完整
    # Merge performance data, English and Chinese into the log, ensuring complete export
    full_log_entry = f"LAT:{latency}s | RAM:{mem_used}MB | CPU:{cpu_perc}% | ENG: {eng_res} | CHN: {chn_res}"
    log_chat(user_input, full_log_entry)

# 6. 管理员控制面板 (view/modify配置)
# 6. Administrator Control Panel (view/modify configuration)
if is_admin:
    st.divider()
    st.subheader("🛠️ Administrator Control Panel")

    with st.expander("📝 Edit System Instructions (chatbot_instructions.txt)"):
        st.write("Modify the AI's persona and pedagogical rules.")
        new_instr = st.text_area("Update Instructions:", value=system_instruction, height=200)
        if st.button("💾 Save & Apply Changes"):
            save_instructions(new_instr)
            st.success("Instructions updated successfully!")
            st.rerun()

    with st.expander("📂 View & Export System Logs"):
        if os.path.exists(LOG_FILE):
            try:
                column_names = ["Timestamp", "User_Message", "Bot_Response"]
                df = pd.read_csv(
                    LOG_FILE,
                    names=column_names,
                    header=None,
                    quoting=csv.QUOTE_ALL,
                    encoding='utf-8-sig'
                )

                # Excel 导出按钮
                # Excel Export
                excel_data = get_excel_data(df)
                st.download_button(
                    label="📥 Download Professional Excel Report",
                    data=excel_data,
                    file_name="academic_tutor_logs.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                # 在线预览
                # Online Preview
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading logs: {e}")
        else:
            st.info("No interaction logs found yet.")
