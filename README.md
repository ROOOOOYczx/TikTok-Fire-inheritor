# TikTok Fire Inheritor

一个基于 [Playwright](https://playwright.dev/python/) 的抖音自动续火脚本。

项目会使用本地 Chrome 浏览器和已保存的登录 Cookies，打开抖音并向指定联系人发送自动生成或自定义的续火消息。

## 功能

- 手动登录抖音并将登录状态保存到 `cookies.json`
- 使用 Cookies 自动打开抖音
- 向配置的联系人发送续火消息
- 支持按当前时间自动生成消息
- 支持自定义固定消息
- 发生页面访问错误时保存截图，便于排查问题

## 环境要求

- Windows
- Python 3.9 或更高版本
- 已安装 Google Chrome
- 可正常访问抖音

安装 Python 依赖：

```bash
pip install playwright
```

项目配置使用 `channel: "chrome"`，因此需要本机已安装 Chrome。若改为使用 Playwright 管理的 Chromium，可将配置中的浏览器启动方式相应调整，并执行：

```bash
playwright install
```

## 使用方法

### 1. 获取 Cookies

首次运行时，先执行：

```bash
python cookies-getter.py
```

脚本会打开抖音页面。请在浏览器中手动完成登录，然后回到终端按回车，脚本会将 Cookies 保存为项目根目录下的 `cookies.json`。

### 2. 配置联系人和消息

编辑 `config.json`：

```json
{
  "browser": {
    "channel": "chrome",
    "headless": false,
    "args": ["--disable-blink-features=AutomationControlled"]
  },
  "receiver_name": "联系人名称",
  "message": {
    "type": "auto_fire",
    "custom_text": "自定义消息",
    "date_format": "%Y年%m月%d日  %H:%M:%S"
  },
  "wait_time_before_close": 10000,
  "timeout": 150000
}
```

消息配置说明：

- `message.type` 为 `auto_fire` 时，使用 `date_format` 按当前时间生成消息
- `message.type` 为 `custom` 时，发送 `message.custom_text`
- `receiver_name` 为抖音私信联系人名称
- `wait_time_before_close` 和 `timeout` 的单位均为毫秒

### 3. 执行自动续火

```bash
python main.py
```

浏览器会以可见模式打开，脚本执行结束后会等待一段时间再关闭浏览器。

## 文件说明

| 文件 | 说明 |
| --- | --- |
| `main.py` | 自动登录并发送续火消息 |
| `cookies-getter.py` | 手动登录并导出 Cookies |
| `config.json` | 浏览器、联系人和消息配置 |
| `cookies.json` | 登录 Cookies，属于敏感信息 |
| `error_*.png` | 页面访问异常时生成的截图 |

## 安全注意事项

- `cookies.json` 等同于登录凭据，请勿公开、上传或分享。
- 不要将真实 Cookies 提交到 Git 仓库或发送给他人。
- 如果 Cookies 失效，请重新运行 `cookies-getter.py` 获取。
- 请遵守抖音的用户协议及相关法律法规，合理使用自动化脚本。

## 常见问题

### 浏览器无法启动

确认 Chrome 已安装，并且 `config.json` 中的 `browser.channel` 与本机浏览器环境匹配。

### 提示 Cookies 不存在或格式错误

确认已在项目根目录生成 `cookies.json`，并且文件内容是有效的 JSON 数组。

### 找不到联系人或页面元素

抖音页面结构可能发生变化。此时请检查联系人名称是否完全匹配，并根据最新页面结构调整 `main.py` 中的元素定位逻辑。

