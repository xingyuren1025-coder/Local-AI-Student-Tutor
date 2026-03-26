# test_ui.py
from playwright.sync_api import sync_playwright
import time


def run_automated_test():
    with sync_playwright() as p:
        print("Starting Automated UI Test...")
        # 启动浏览器（headless=False 可以让你亲眼看到脚本在打字）
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 访问本地运行的 Streamlit 地址
        page.goto("http://localhost:8501")

        # 1. 测试提问功能
        input_placeholder = "Ask a technical question..."
        page.get_by_placeholder(input_placeholder).fill("Explain VLAN in networking")
        page.get_by_placeholder(input_placeholder).press("Enter")

        print("Waiting for AI response (this may take a while)...")
        # 等待双栏响应出现，超时时间设为 30秒
        time.sleep(20)

        # 2. 验证页面是否显示了预期的双栏标题
        if "English Response" in page.content() and "中文翻译" in page.content():
            print("✅ Success: Dual-language layout detected!")
        else:
            print("❌ Failure: Response columns not found.")

        # 3. 截图作为论文证据 (Evidence for Chapter 5)
        page.screenshot(path="test_results_screenshot.png")
        print("Screenshot saved as test_results_screenshot.png")

        browser.close()


if __name__ == "__main__":
    run_automated_test()