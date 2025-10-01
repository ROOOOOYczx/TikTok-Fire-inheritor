import os
import json
from playwright.sync_api import sync_playwright, Playwright

def get_and_save_cookies(target_url: str, cookie_file: str):
    """
    启动浏览器，用户手动登录，然后保存cookies到JSON文件。
    """
    with sync_playwright() as p:

        browser = p.chromium.launch(channel="chrome",headless=False)
        context = browser.new_context()    
        page = context.new_page()
        try:
            print(f"正在打开页面: {target_url}")
            page.goto(target_url, timeout=60000) # 设置60秒超时
            
            # 提示用户进行登录操作
            print("\n================================================================================")
            print("浏览器已打开，请在浏览器中手动完成登录操作。")
            print("登录成功后，回到此终端窗口，然后按【回车键】继续...")
            print("================================================================================")
            
            # 等待用户在终端按回车键
            input()
            
            # 用户确认登录后，获取当前上下文的cookies
            print("\n正在获取 Cookies...")
            cookies = context.cookies()
            

            # 1. 检查同名文件是否存在，如果存在则删除
            if os.path.exists(cookie_file):
                print(f"发现已存在的旧 Cookies 文件: '{cookie_file}'，正在删除...")
                os.remove(cookie_file)
                print("旧文件已删除。")
            
            # 2. 将获取到的cookies保存为JSON文件
            with open(cookie_file, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, indent=4) # indent=4 让JSON文件格式更美观
            
            print(f"\n Cookies 已成功获取并保存到文件: '{cookie_file}'")

        except Exception as e:
            print(f"发生错误: {e}")
            
        finally:
            print("正在关闭浏览器...")
            browser.close()
            print("程序执行完毕。")

if __name__ == "__main__":
    # --- 配置区域 ---

    TARGET_URL = "https://douyin.com/"  
    COOKIE_FILE = "cookies.json"        
    get_and_save_cookies(TARGET_URL, COOKIE_FILE)