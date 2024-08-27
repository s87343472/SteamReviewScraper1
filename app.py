import time
import json
import pandas as pd
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading
import random

app = Flask(__name__)
socketio = SocketIO(app)
scraping_active = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_scrape', methods=['POST'])
def start_scrape():
    game_id = request.form['game_id']
    global scraping_active
    scraping_active = True
    thread = threading.Thread(target=scrape_steam_reviews, args=(game_id,))
    thread.start()
    return '', 200

@app.route('/stop_scrape', methods=['POST'])
def stop_scrape():
    global scraping_active
    scraping_active = False
    return '', 200

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('.', filename, as_attachment=True)

def scrape_steam_reviews(game_id):
    global scraping_active

    socketio.emit('log_message', f"Starting scraping for game ID: {game_id}")

    options = webdriver.ChromeOptions()
    # 使用无头模式
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = f"https://steamcommunity.com/app/{game_id}/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=all#"
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    try:
        view_page_button = driver.find_element(By.XPATH, "//span[text()='浏览社区中心']")
        view_page_button.click()
        socketio.emit('log_message', "Clicked on 浏览社区中心 button.")
        time.sleep(5)
    except Exception as e:
        socketio.emit('log_message', "No age verification needed or failed to find the button.")

    reviews = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    while scraping_active:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_sleep = random.uniform(5, 7)
        time.sleep(random_sleep)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            socketio.emit('log_message', "All reviews loaded.")
            break
        last_height = new_height

        review_elements = driver.find_elements(By.CLASS_NAME, "apphub_Card")
        for review_element in review_elements:
            try:
                username = review_element.find_element(By.CLASS_NAME, "apphub_CardContentAuthorName").text
                playtime = review_element.find_element(By.CLASS_NAME, "hours").text
                content = review_element.find_element(By.CLASS_NAME, "apphub_CardTextContent").text
                recommended = "推荐" if "Recommended" in review_element.find_element(By.CLASS_NAME, "title").text else "不推荐"

                reviews.append({
                    "username": username,
                    "playtime": playtime,
                    "content": content,
                    "recommended": recommended
                })

                if len(reviews) % 100 == 0:
                    socketio.emit('log_message', f"抓取了 {len(reviews)} 条评论")
                    # 间歇性的保存抓取的数据
                    save_reviews_to_file(game_id, reviews)

            except Exception as e:
                socketio.emit('log_message', f"Error while parsing a review: {str(e)}")

        if not scraping_active:
            break

    driver.quit()
    socketio.emit('log_message', f"抓取完成，共抓取 {len(reviews)} 条评论")
    save_reviews_to_file(game_id, reviews)
    socketio.emit('download_ready', {'filename': f"{game_id}_reviews.xlsx"})

def save_reviews_to_file(game_id, reviews):
    json_file = f"{game_id}_reviews.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)

    df = pd.DataFrame(reviews)
    excel_file = f"{game_id}_reviews.xlsx"
    df.to_excel(excel_file, index=False)

if __name__ == '__main__':
    socketio.run(app, debug=True)