import csv
import os
import pandas as pd
import io
from datetime import datetime
from config_manager import LOG_FILE


# 函数 1：记录聊天到 CSV
# Record Chat to CSV
def log_chat(user_msg, bot_reply):
    file_exists = os.path.isfile(LOG_FILE)
    # 使用 utf-8-sig 确保 Excel 打开不乱码
    # Use utf-8-sig to ensure Excel opens without garbled text
    with open(LOG_FILE, mode="a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        if not file_exists:
            writer.writerow(["Timestamp", "User_Message", "Bot_Response"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), user_msg, bot_reply])


# 函数 2：导出 Excel
# Export to Excel
def get_excel_data(df):
    buffer = io.BytesIO()
    # 使用 xlsxwriter 引擎使表格更专业
    # Use the xlsxwriter to make more professional
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='ChatLogs')
        workbook = writer.book
        worksheet = writer.sheets['ChatLogs']

        # 设置专业表格样式
        # Set professional table style
        header_fmt = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
        cell_fmt = workbook.add_format({'text_wrap': True, 'valign': 'top', 'border': 1})

        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_fmt)

        # 设置列宽，让表格更整齐
        # Set column width to make the table neater
        worksheet.set_column('A:A', 20, cell_fmt)  # Timestamp
        worksheet.set_column('B:B', 30, cell_fmt)  # User Message
        worksheet.set_column('C:C', 100, cell_fmt)  # Bot Response

    return buffer.getvalue()
