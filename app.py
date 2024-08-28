from scraper import scrape_steam_reviews
import threading
import queue
from flask import Flask, request, render_template, send_from_directory, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'output'

scrape_thread = None
progress = 0
is_scraping = False
result_queue = queue.Queue()
log_queue = queue.Queue(maxsize=100)

scrape_lock = threading.Lock()

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/scrape', methods=['POST'])
def scrape():
    global is_scraping, scrape_thread
    game_id = request.form['game_id']
    max_reviews = int(request.form.get('max_reviews', 1000000))
    max_time = int(request.form.get('max_time', 3600))

    if is_scraping:
        return jsonify({"error": "已经有一个抓取任务在进行中"}), 400

    is_scraping = True

    def scrape_task():
        global is_scraping
        try:
            json_filename, excel_filename = scrape_steam_reviews(
                game_id, 
                progress_callback=update_progress, 
                log_callback=update_log, 
                max_reviews=max_reviews, 
                max_time=max_time,
                stop_check=lambda: not is_scraping
            )
            if json_filename and excel_filename:
                result_queue.put({
                    "success": "抓取完成",
                    "json_file": json_filename,
                    "excel_file": excel_filename
                })
            else:
                result_queue.put({"error": "抓取失败，未生成文件"})
        except Exception as e:
            update_log(f"抓取任务出错: {str(e)}")
            result_queue.put({"error": f"抓取任务出错: {str(e)}"})
        finally:
            is_scraping = False
            update_log("抓取任务结束")

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
    with scrape_lock:
        if is_scraping:
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

def update_progress(current, total):
    global progress
    progress = int((current / total) * 100) if total > 0 else 0

def update_log(message):
    log_queue.put(message[:1000])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5013)