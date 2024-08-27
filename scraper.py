import time
import json
import random
import pandas as pd
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 配置参数
MAX_REVIEWS = 50000
MAX_SCROLL_ATTEMPTS = 100
SCROLL_PAUSE_TIME = 2

stop_flag = False

def scrape_steam_reviews(game_id, progress_callback=None, log_callback=None):
    global stop_flag
    stop_flag = False
    
    if log_callback:
        log_callback(f"开始抓取游戏ID为 {game_id} 的评论")
    
    url = f"https://steamcommunity.com/app/{game_id}/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=all"
    
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    game_name = get_game_name(soup)
    total_reviews = []
    cursor = '*'

    while len(total_reviews) < MAX_REVIEWS and not stop_flag:
        params = {
            'cursor': cursor,
            'day_range': 365,
            'start_offset': 0,
            'review_type': 'all',
            'purchase_type': 'all'
        }
        
        api_url = f"https://steamcommunity.com/app/{game_id}/reviews/render/"
        response = session.get(api_url, params=params)
        data = response.json()

        if not data['success']:
            break

        new_reviews = extract_reviews(data['html'])
        total_reviews.extend(new_reviews)

        if progress_callback:
            progress_callback(len(total_reviews), MAX_REVIEWS)

        if log_callback:
            log_callback(f"已抓取 {len(total_reviews)} 条评论")

        cursor = data['cursor']
        if not cursor:
            break

        time.sleep(random.uniform(SCROLL_PAUSE_TIME, SCROLL_PAUSE_TIME + 2))

    return save_reviews(game_id, game_name, total_reviews)

def get_game_name(soup):
    try:
        return soup.find('div', class_='apphub_AppName').text
    except:
        return "Unknown Game"

def extract_reviews(html):
    soup = BeautifulSoup(html, 'html.parser')
    reviews = soup.find_all('div', class_='apphub_Card')
    extracted_reviews = []

    for review in reviews:
        try:
            review_data = extract_review_data(review)
            extracted_reviews.append(review_data)
        except Exception as e:
            logging.warning(f"解析评论时出错: {str(e)}")

    return extracted_reviews

def extract_review_data(review):
    return {
        "username": review.find('div', class_='apphub_CardContentAuthorName').text.strip(),
        "playtime": review.find('div', class_='hours').text.strip(),
        "content": review.find('div', class_='apphub_CardTextContent').text.strip(),
        "recommended": "推荐" if "推荐" in review.find('div', class_='title').text else "不推荐",
        "time_info": review.find('div', class_='date_posted').text.strip(),
        "owned_products": review.find('div', class_='apphub_CardContentMoreLink').text.strip(),
        "found_helpful": review.find('div', class_='found_helpful').text.strip()
    }

def save_reviews(game_id, game_name, reviews):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_prefix = f"{game_name}_{game_id}_{timestamp}"
    
    json_file = f"output/{file_prefix}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)
    
    df = pd.DataFrame(reviews)
    excel_file = f"output/{file_prefix}.xlsx"
    df.to_excel(excel_file, index=False)

    logging.info(f"评论已保存到 {json_file} 和 {excel_file}")

    return json_file, excel_file

def stop_scraping():
    global stop_flag
    stop_flag = True
    logging.info("收到停止抓取信号")

if __name__ == "__main__":
    game_id = input("请输入Steam游戏ID: ")
    scrape_steam_reviews(game_id)