from flask import Flask, request, render_template, send_from_directory, jsonify
import os
from scraper import scrape_steam_reviews, stop_scraping
import re
from datetime import datetime
import threading
import queue

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'output'

scrape_thread = None
progress = 0
is_scraping = False
result_queue = queue.Queue()
log_queue = queue.Queue(maxsize=100)

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/scrape', methods=['POST'])
def scrape():
    global scrape_thread, progress, is_scraping
    game_id = request.form['game_id']
    if not game_id or not re.match(r'^\d+$', game_id):
        return jsonify({"error": "请提供有效的Steam游戏ID（仅数字）"}), 400
    
    if is_scraping:
        return jsonify({"error": "已有抓取任务正在进行中"}), 400

    is_scraping = True
    progress = 0
    
    def scrape_task():
        global progress, is_scraping
        try:
            json_file, excel_file = scrape_steam_reviews(game_id, progress_callback, log_callback)
            files = os.listdir(app.config['UPLOAD_FOLDER'])
            result_queue.put({"success": "抓取完成", "files": files})
        except Exception as e:
            result_queue.put({"error": f"抓取过程中出错：{str(e)}"})
        finally:
            is_scraping = False

    scrape_thread = threading.Thread(target=scrape_task)
    scrape_thread.start()
    return jsonify({"success": "抓取任务已开始"})

@app.route('/progress')
def get_progress():
    global progress, is_scraping
    return jsonify({"progress": progress, "is_scraping": is_scraping})

@app.route('/stop', methods=['POST'])
def stop():
    global is_scraping
    if is_scraping:
        stop_scraping()
        is_scraping = False
        return jsonify({"success": "抓取任务已停止"})
    else:
        return jsonify({"error": "没有正在进行的抓取任务"}), 400

@app.route('/download/<filename>')
def download_file(filename):
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return jsonify({"error": "文件不存在"}), 404
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/result')
def get_result():
    if not result_queue.empty():
        return jsonify(result_queue.get())
    return jsonify({"status": "pending"})

@app.route('/logs')
def get_logs():
    logs = []
    while not log_queue.empty():
        logs.append(log_queue.get())
    return jsonify(logs)

def progress_callback(current, total):
    global progress
    progress = int((current / total) * 100)

def log_callback(message):
    log_queue.put(message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)