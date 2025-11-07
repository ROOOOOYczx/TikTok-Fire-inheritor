import json
import datetime as dt
from playwright.sync_api import sync_playwright
from datetime import datetime
import time
import argparse

def load_config(config_file='config.json'):
    """加载配置文件"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{config_file} 文件未找到，使用默认配置")
        return {
            "browser": {
                "channel": "msedge",
                "headless": False,
                "args": ["--disable-blink-features=AutomationControlled"]
            },
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "viewport": {
                "width": 1920,
                "height": 1080
            },
            "receiver_name": "666不喜欢填",
             "message": {
                "type": "auto_fire", 
                "//type":"可选择auto_fire(自动续火) 或 custom(自定义)     当type为custom时使用的自定义文本",
                "custom_text": "无敌了孩子",   
                "date_format": "%Y年%m月%d日  %H:%M:%S"
            },
            "wait_time_before_close": 10000,
            "timeout": 5000
        }
    except json.JSONDecodeError:
        print(f"{config_file} 文件格式错误，使用默认配置")
        return None

def get_auto_fire_message(date_format="%Y年%m月%d日"):        #生成自动续火消息
    current_date = dt.datetime.now().strftime(date_format)
    return f"[自动续火] {current_date}"

def douyin_auto_login(config_file='config.json', cookies_file='cookies.json'):
    config = load_config(config_file)
    if config is None:
        return
    

    if config["message"] == "auto_fire":# 使用自动生成的消息
        message_to_send = get_auto_fire_message()
    else:# 使用配置的固定消息
        message_to_send = config["message"]

    # 初始化 Playwright
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(
            channel=config["browser"]["channel"],
            headless=config["browser"]["headless"],
            args=config["browser"]["args"]  
        )
        
        # 创建浏览器上下文
        context = browser.new_context(
            user_agent=config["user_agent"],
            viewport=config["viewport"]
        )
        
        # 从 cookies 文件加载 cookies
        try:
            with open(cookies_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            
            # 添加 cookies 到浏览器上下文
            context.add_cookies(cookies)
            print(f"Cookies 加载成功！(文件: {cookies_file})")
        except FileNotFoundError:
            print(f"{cookies_file} 文件未找到，请确保文件存在")
            return
        except json.JSONDecodeError:
            print(f"{cookies_file} 文件格式错误")
            return
        
        # 创建新页面
        page = context.new_page()
        
        try:
            print("正在打开抖音网页...")
            page.goto('https://www.douyin.com/?recommend=1', timeout=config["timeout"])
            
            # 等待页面加载
            page.wait_for_timeout(1000)
            html_content = page.content()

            if "未登录" in html_content:
                login_state = False
            else:
                login_state = True
            # 检查是否成功登录

            if login_state == True:
                print("登录成功！检测到用户信息。")
                cancel_button = page.get_by_text("取消")
                # 进行续火操作
                if cancel_button.is_visible():
                    cancel_button.click()

                message_button = page.get_by_text("私信")
                message_button.click()
                
                page.wait_for_timeout(5000)
                # 使用配置的接收者名称
                receiver_name = page.locator(f'div:text-is("{config["receiver_name"]}")')
                if receiver_name.is_visible():
                    print(f"找到了续火人: {config['receiver_name']}")
                    receiver_name.click()
                    page.wait_for_timeout(5000)

                    if config["message"]["type"] == "auto_fire":
                        date_format = config["message"].get("date_format", "%Y年%m月%d日")
                        message_to_send = get_auto_fire_message(date_format)
                    else:
                         message_to_send = config["message"]["custom_text"]

                    page.keyboard.type(message_to_send, delay=100)
                    page.keyboard.press('Enter')
                    print("发送成功")
                else:
                    print(f"未找到续火人: {config['receiver_name']}")
            else:
                print("未能自动登录，可能需要手动登录或更新 cookies")
            
            # 保持浏览器打开一段时间以便观察
            print(f"页面将在{config['wait_time_before_close']//1000}秒后关闭...")
            page.wait_for_timeout(config["wait_time_before_close"])
            
        except Exception as e:
            print(f"访问页面时出错: {e}")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"error_{timestamp}.png"     # 截图保存错误状态
            page.screenshot(path=filename)           
            print(f"已保存错误截图到 {filename}")
        
        finally:
            browser.close()

def run_scheduled_task(config_file='config.json', cookies_file='cookies.json'):
    """持续运行，每天凌晨4点执行任务"""
    last_run_date = None
    
    print("=" * 50)
    print("程序已启动，将在每天凌晨4点自动执行任务")
    print(f"配置文件: {config_file}")
    print(f"Cookies文件: {cookies_file}")
    print("=" * 50)
    
    while True:
        try:
            now = datetime.now()
            current_date = now.date()
            current_hour = now.hour
            current_minute = now.minute
            
            # 检查是否到达凌晨4点（4:00-4:01之间）且今天还未执行过
            if current_hour == 4 and current_minute == 0 and last_run_date != current_date:
                print(f"\n[{now.strftime('%Y-%m-%d %H:%M:%S')}] 开始执行定时任务...")
                douyin_auto_login(config_file, cookies_file)
                last_run_date = current_date
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 任务执行完成，等待下一次执行...")
            
            # 每分钟检查一次时间
            time.sleep(60)
            
        except KeyboardInterrupt:
            print("\n程序已被用户中断")
            break
        except Exception as e:
            print(f"运行出错: {e}")
            print("60秒后继续...")
            time.sleep(60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='抖音自动续火程序 - 每天凌晨4点自动执行')
    parser.add_argument('--config', '-c', 
                        default='config.json', 
                        help='配置文件路径 (默认: config.json)')
    parser.add_argument('--cookies', '-k', 
                        default='cookies.json', 
                        help='Cookies文件路径 (默认: cookies.json)')
    parser.add_argument('--run-now', '-r', 
                        action='store_true', 
                        help='立即执行一次任务（不等待定时）')
    
    args = parser.parse_args()
    
    if args.run_now:
        print("=" * 50)
        print("立即执行模式")
        print(f"配置文件: {args.config}")
        print(f"Cookies文件: {args.cookies}")
        print("=" * 50)
        douyin_auto_login(args.config, args.cookies)
    else:
        run_scheduled_task(args.config, args.cookies)






