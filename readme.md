# Steam 评论抓取器

这是一个用于抓取 Steam 游戏评论的 Web 应用程序。该应用使用 Flask 框架构建，并使用 requests 和 BeautifulSoup 来抓取 Steam 评论。

## 功能特点

- 通过 Steam 游戏 ID 抓取游戏评论
- 实时显示抓取进度
- 支持停止正在进行的抓取任务
- 将抓取的评论保存为 JSON 和 Excel 格式
- 提供下载抓取结果的功能

## 环境要求

- Python 3.7+
- pip (Python 包管理器)

## 安装步骤

1. 克隆仓库：
   ```
   git clone https://github.com/your-username/steam-review-scraper.git
   cd steam-review-scraper
   ```

2. 创建虚拟环境（推荐）：
   ```
   python -m venv venv
   ```

3. 激活虚拟环境：
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

## 配置

1. 创建 `output` 目录用于存储抓取结果：
   ```
   mkdir output
   ```

2. 如果需要，可以在 `app.py` 中修改端口号（默认为 5013）。

## 运行应用

1. 确保您在项目目录中并已激活虚拟环境。

2. 运行 Flask 应用：
   ```
   python app.py
   ```

3. 在浏览器中打开 `http://localhost:5013` 以访问应用程序。

## 使用说明

1. 在网页界面输入 Steam 游戏 ID（纯数字）。
2. 点击"开始抓取"按钮开始抓取评论。
3. 抓取过程中可以查看进度和日志。
4. 如需停止抓取，点击"停止抓取"按钮。
5. 抓取完成后，可以在文件列表中下载 JSON 或 Excel 格式的结果文件。

## 项目结构

- `app.py`: Flask 应用主文件
- `scraper.py`: 评论抓取逻辑
- `templates/index.html`: 网页界面模板
- `output/`: 存储抓取结果的目录

## 注意事项

- 请遵守 Steam 的使用条款和政策。
- 大量或频繁的请求可能会被 Steam 限制，请合理使用。

## 贡献

欢迎提交 issues 和 pull requests 来改进这个项目。

## 许可

[MIT License](LICENSE)
