# Steam 评论抓取器

这是一个用于抓取 Steam 游戏评论的 Web 应用程序。

## 环境要求

- Python 3.7+
- Chrome 浏览器（用于 Selenium）

## 安装步骤

### 通用步骤

1. 克隆仓库：
   ```
   git clone https://github.com/your-username/steam-review-scraper.git
   cd steam-review-scraper
   ```

2. 创建虚拟环境（可选但推荐）：
   ```
   python -m venv venv
   ```

3. 激活虚拟环境：

   - Windows:
     ```
     venv\Scripts\activate
     ```
   
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

### 特定操作系统步骤

#### Windows

1. 下载并安装 Chrome 浏览器（如果尚未安装）。
2. 下载与您的 Chrome 版本匹配的 ChromeDriver，并将其添加到系统 PATH 中。

#### macOS

1. 使用 Homebrew 安装 Chrome（如果尚未安装）：
   ```
   brew install --cask google-chrome
   ```
2. 安装 ChromeDriver：
   ```
   brew install chromedriver
   ```

#### Linux (Ubuntu/Debian)

1. 安装 Chrome：
   ```
   sudo apt update
   sudo apt install google-chrome-stable
   ```
2. 下载与您的 Chrome 版本匹配的 ChromeDriver，并将其添加到系统 PATH 中。

## 启动应用

1. 确保您在项目目录中并已激活虚拟环境。

2. 运行 Flask 应用：
   ```
   python app.py
   ```

3. 在浏览器中打开 `http://127.0.0.1:5000` 以访问应用程序。
