# Steam 评论抓取工具v1.2

这是一个用于抓取 Steam 游戏评论的工具。它使用 Python 和 Selenium 来自动化抓取过程,并提供了一个简单的 Web 界面来控制抓取任务。

## 功能特点

- 自动抓取指定游戏的 Steam 评论
- 支持设置最大评论数和最大抓取时间
- 结果保存为 JSON 和 Excel 格式
- 提供 Web 界面来控制抓取任务和查看进度

## 系统要求

- Windows 操作系统
- Python 3.7 或更高版本
- Google Chrome 浏览器

## 安装说明

1. 确保您的系统已安装 Python 3.7 或更高版本。
2. 下载并安装与您的 Chrome 浏览器版本匹配的 ChromeDriver,将其放置在系统 PATH 中或项目目录下。
3. 在项目根目录下创建一个名为 `output` 的文件夹,用于存储生成的文件。

## 使用方法

1. 将所有项目文件放在同一目录下。
2. 双击运行 `run_server.bat`。
   - 首次运行时,脚本会自动创建虚拟环境并安装所需依赖。
   - 之后的运行将直接启动服务器。
3. 打开浏览器,访问 `http://localhost:5013` 来使用 Web 界面。

## 文件说明

- `run_server.bat`: 主要的批处理文件,用于设置环境和启动服务器。
- `app.py`: Flask 应用程序,提供 Web 界面和 API。
- `scraper.py`: 包含抓取 Steam 评论的核心逻辑。
- `requirements.txt`: 列出了项目所需的 Python 依赖。

## 注意事项

- 确保您的网络连接稳定,以便能够访问 Steam 网站。
- 抓取大量评论可能需要较长时间,请耐心等待。
- 请遵守 Steam 的使用条款和服务条款。
- 如果遇到 "无法加载更多评论" 的提示,可能是因为已经抓取了该游戏的所有可用评论。

## 故障排除

- 如果遇到 ChromeDriver 相关错误,请确保已安装正确版本的 ChromeDriver。
- 如果依赖安装失败,请检查您的网络连接,或尝试手动安装 `requirements.txt` 中列出的包。

## 贡献

欢迎提交问题报告和改进建议。如果您想贡献代码,请先开 issue 讨论您的想法。

## 许可证

[MIT License](https://opensource.org/licenses/MIT)
