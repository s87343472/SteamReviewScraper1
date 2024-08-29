from flask import Flask, render_template, request, jsonify, send_from_directory
from scraper import scrape_steam_reviews
import os
import threading
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 配置
app.config['UPLOAD_FOLDER'] = 'output'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 全局变量
scraping_thread = None
is_scraping = False
progress = 0
reviews_count = 0
game_id = None
files_ready = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def start_scrape():
    global scraping_thread, is_scraping, progress, reviews_count, game_id, files_ready
    
    if is_scraping:
        return jsonify({"error": "已经有一个抓取任务在进行中"}), 400
    
    game_id = request.json.get('game_id')
    if not game_id:
        return jsonify({"error": "缺少游戏ID"}), 400
    
    is_scraping = True
    progress = 0
    reviews_count = 0
    files_ready = False
    
    def scrape_function(game_id):
        global progress, reviews_count, is_scraping, files_ready
        try:
            scrape_steam_reviews(game_id, progress_callback=update_progress, log_callback=add_log, stop_check=lambda: not is_scraping)
        except Exception as e:
            add_log(f"抓取过程中出现错误: {str(e)}", True)
        finally:
            is_scraping = False
            files_ready = True
    
    scraping_thread = threading.Thread(target=scrape_function, args=(game_id,))
    scraping_thread.start()
    
    return jsonify({"message": "抓取任务已开始"}), 200

@app.route('/stop', methods=['POST'])
def stop_scrape():
    global is_scraping
    if is_scraping:
        is_scraping = False
        return jsonify({"message": "正在停止抓取任务"}), 200
    else:
        return jsonify({"message": "没有正在进行的抓取任务"}), 400

@app.route('/progress')
def get_progress():
    global progress, reviews_count
    return jsonify({"progress": progress, "reviews_count": reviews_count})

@app.route('/result')
def get_result():
    global is_scraping, game_id
    if is_scraping:
        return jsonify({"status": "scraping", "game_id": game_id})
    elif game_id:
        return jsonify({"status": "completed", "game_id": game_id})
    else:
        return jsonify({"status": "idle"})

@app.route('/files')
def list_files():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 每页显示的文件数量

    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith('.json') or filename.endswith('.xlsx'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(file_path):
                parts = filename.split('_')
                if len(parts) >= 2:
                    game_id = parts[-2]  # 假设游戏ID是倒数第二个部分
                    files.append({
                        'name': filename,
                        'size': os.path.getsize(file_path),
                        'modified': os.path.getmtime(file_path),
                        'game_id': game_id
                    })
    
    # 按修改时间倒序排序
    files.sort(key=lambda x: x['modified'], reverse=True)
    
    # 计算总页数
    total_pages = (len(files) + per_page - 1) // per_page
    
    # 获取当前页的文件
    start = (page - 1) * per_page
    end = start + per_page
    current_files = files[start:end]
    
    return jsonify({
        'files': current_files,
        'total_pages': total_pages,
        'current_page': page
    })

@app.route('/output/<path:filename>')
def download_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        return f"文件下载失败: {str(e)}", 500

@app.route('/files_status')
def get_files_status():
    global files_ready
    return jsonify({"ready": files_ready})

def update_progress(progress_value, reviews_count_value):
    global progress, reviews_count
    progress = progress_value
    reviews_count = reviews_count_value

def add_log(message, is_error=False):
    print(f"{'ERROR: ' if is_error else ''}{message}")

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5013)