from flask import Flask, request, send_file, render_template
import os
from scraper import scrape_steam_reviews, stop_scraping

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    game_id = request.form['game_id']
    if not game_id:
        return "请提供有效的Steam游戏ID", 400
    
    # 调用scraper.py中的函数进行评论抓取
    json_file = scrape_steam_reviews(game_id)
    
    # 提供下载功能
    return send_file(json_file, as_attachment=True)

@app.route('/stop_scrape', methods=['POST'])
def stop_scrape():
    stop_scraping()  # 终止抓取
    return "停止抓取成功"

if __name__ == '__main__':
    app.run(debug=True)