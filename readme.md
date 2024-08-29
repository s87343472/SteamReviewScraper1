# Steam 评论抓取工具

这是一个用于抓取 Steam 游戏评论的工具。它使用 Python、Selenium 和 Flask 来自动化抓取过程，并提供了一个简单的 Web 界面来控制抓取任务。

## 功能特点

* 自动抓取指定游戏的 Steam 评论
* 支持设置最大评论数和最大抓取时间
* 结果保存为 JSON 和 Excel 格式
* 提供 Web 界面来控制抓取任务和查看进度
* 优化的日志输出，减少重复信息

## 系统要求

* Windows 操作系统
* Python 3.7 或更高版本
* Google Chrome 浏览器

## 安装说明

1. 确保您的系统已安装 Python 3.7 或更高版本。
2. 下载并安装与您的 Chrome 浏览器版本匹配的 ChromeDriver，将其放置在系统 PATH 中或项目目录下。
3. 在项目根目录下创建一个名为 `output` 的文件夹，用于存储生成的文件。
4. 克隆仓库：
   ```bash
   git clone https://github.com/s87343472/SteamReviewScraper1.git
   cd SteamReviewScraper1
   ```

5. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

1. 运行 `run_server.bat` 或执行以下命令启动服务器：
   ```bash
   python app.py
   ```

2. 打开浏览器，访问 `http://localhost:5013` 来使用 Web 界面。
3. 输入 Steam 游戏 ID，设置最大评论数和最大抓取时间（可选），然后点击"开始抓取"。
4. 抓取完成后，可以在 Web 界面下载生成的 JSON 和 Excel 文件。

## 文件说明

* `app.py`: Flask 应用程序，提供 Web 界面和 API。
* `scraper.py`: 包含抓取 Steam 评论的核心逻辑。
* `requirements.txt`: 列出了项目所需的 Python 依赖。
* `run_server.bat`: Windows 批处理脚本，用于快速启动服务器。

## 最新更新

* 优化了日志输出，减少了重复信息。
* 改进了前端界面，只在评论数量变化时更新显示。
* 调整了后端逻辑，提高了抓取效率。

## 注意事项

* 确保您的网络连接稳定，以便能够访问 Steam 网站。
* 抓取大量评论可能需要较长时间，请耐心等待。
* 请遵守 Steam 的使用条款和服务条款。
* 如果遇到 "无法加载更多评论" 的提示，可能是因为已经抓取了该游戏的所有可用评论。

## 故障排除

* 如果遇到 ChromeDriver 相关错误，请确保已安装正确版本的 ChromeDriver。
* 如果依赖安装失败，请检查您的网络连接，或尝试手动安装 `requirements.txt` 中列出的包。

## 贡献

欢迎提交问题报告和改进建议。如果您想贡献代码，请先开 issue 讨论您的想法。

## 许可证

[MIT License](https://opensource.org/licenses/MIT)

## 项目结构

```
SteamReviewScraper/
│
├── app.py # Flask 应用主文件
├── scraper.py # 评论抓取核心逻辑
├── requirements.txt # 项目依赖列表
├── run_server.bat # Windows 批处理脚本，用于设置环境和启动服务器
├── README.md # 项目说明文档
├── .gitignore # Git 忽略文件配置
├── templates/ # HTML 模板文件夹
│ └── index.html # 主页面模板
├── static/ # 静态文件文件夹（如果有的话）
│ ├── css/
│ ├── js/
│ └── img/
└── output/ # 输出文件夹，存储抓取结果

## 注意事项

- 确保您的网络连接稳定，以便能够访问 Steam 网站。
- 抓取大量评论可能需要较长时间，请耐心等待。
- 请遵守 Steam 的使用条款和服务条款。
- 如果遇到 "无法加载更多评论" 的提示，可能是因为已经抓取了该游戏的所有可用评论。

## 故障排除

- 如果遇到 ChromeDriver 相关错误，请确保已安装正确版本的 ChromeDriver。
- 如果依赖安装失败，请检查您的网络连接，或尝试手动安装 `requirements.txt` 中列出的包。

## 贡献

欢迎提交问题报告和改进建议。如果您想贡献代码，请先开 issue 讨论您的想法。

## 许可证

[MIT License](https://opensource.org/licenses/MIT)