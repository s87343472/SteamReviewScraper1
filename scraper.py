from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
import pandas as pd
from datetime import datetime
import random
import os
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def scrape_steam_reviews(game_id, progress_callback=None, log_callback=None, max_reviews=1000000, max_time=3600, stop_check=None):
    print(f"开始抓取游戏ID: {game_id}")
    if log_callback:
        log_callback(f"开始抓取游戏ID: {game_id}")
    
    url = f"https://steamcommunity.com/app/{game_id}/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=all"
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(url)
    
    all_reviews = []
    start_time = time.time()
    last_review_count = 0
    no_new_reviews_count = 0
    last_logged_count = 0
    
    try:
        while True:
            if stop_check and stop_check():
                print("抓取任务被手动停止")
                if log_callback:
                    log_callback("抓取任务被手动停止")
                break
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight * Math.random());")
            
            time.sleep(random.uniform(5, 10))  # 在滚动后等待更长时间
            
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "apphub_Card"))
                )
            except:
                print("无法加载更多评论，可能已到达底部")
                if log_callback:
                    log_callback("无法加载更多评论，可能已到达底部")
                break
            
            reviews = driver.find_elements(By.CLASS_NAME, "apphub_Card")
            
            for review in reviews[last_review_count:]:
                try:
                    review_data = {
                        "username": "",
                        "products_count": "",
                        "playtime_hours": 0,
                        "reviews_count": "",
                        "recommendation": "",
                        "content": "",
                        "early_access": False,
                        "received_free": False,
                        "post_date": "",
                        "edit_date": "",
                        "helpful_count": 0,
                        "funny_count": 0,
                        "comments_count": 0,
                        "review_url": ""
                    }

                    # 用户名
                    author_element = review.find_element(By.CLASS_NAME, "apphub_CardContentAuthorName")
                    if author_element:
                        review_data["username"] = author_element.text.strip()

                    # 账户内拥有产品数量
                    products_element = review.find_element(By.CLASS_NAME, "apphub_CardContentMoreLink")
                    if products_element:
                        match = re.search(r"拥有 (\d+) 项产品", products_element.text)
                        if match:
                            review_data["products_count"] = int(match.group(1))

                    # 游玩时长
                    hours_element = review.find_element(By.CLASS_NAME, "hours")
                    if hours_element:
                        match = re.search(r"总时数 ([\d.]+) 小时", hours_element.text)
                        if match:
                            review_data["playtime_hours"] = float(match.group(1))

                    # 推荐/不推荐
                    title_element = review.find_element(By.CLASS_NAME, "title")
                    if title_element:
                        review_data["recommendation"] = "推荐" if "推荐" in title_element.text else "不推荐"

                    # 评测内容和发布时间
                    content_element = review.find_element(By.CLASS_NAME, "apphub_CardTextContent")
                    if content_element:
                        full_text = content_element.text.strip()
                        date_match = re.search(r"发布于：(.+)$", full_text)
                        if date_match:
                            review_data["post_date"] = date_match.group(1).strip()
                            review_data["content"] = full_text[:date_match.start()].strip()
                        else:
                            review_data["content"] = full_text

                    # 是否抢先体验
                    early_access_element = review.find_elements(By.CLASS_NAME, "early_access_review")
                    review_data["early_access"] = len(early_access_element) > 0

                    # 有用性和欢乐评分
                    helpful_element = review.find_element(By.CLASS_NAME, "found_helpful")
                    if helpful_element:
                        helpful_match = re.search(r"有 (\d+) 人觉得这篇评测有价值", helpful_element.text)
                        if helpful_match:
                            review_data["helpful_count"] = int(helpful_match.group(1))
                        funny_match = re.search(r"有 (\d+) 人觉得这篇评测很欢乐", helpful_element.text)
                        if funny_match:
                            review_data["funny_count"] = int(funny_match.group(1))

                    # 评论数量
                    comments_element = review.find_element(By.CLASS_NAME, "apphub_CardCommentCount")
                    if comments_element:
                        review_data["comments_count"] = int(comments_element.text)

                    # 该条测评URL
                    review_link = review.find_element(By.CLASS_NAME, "apphub_CardContentAuthorName").get_attribute("href")
                    if review_link:
                        review_data["review_url"] = review_link

                    all_reviews.append(review_data)

                except Exception as e:
                    print(f"处理单条评论时出错: {str(e)}")
                    if log_callback:
                        log_callback(f"处理单条评论时出错: {str(e)}", True)

            if progress_callback:
                progress = min(len(all_reviews) / max_reviews * 100, 100)
                progress_callback(progress, len(all_reviews))
            
            # 只在评论数量发生变化时更新日志
            if len(all_reviews) != last_logged_count:
                print(f"已抓取 {len(all_reviews)} 条评论")
                if log_callback:
                    log_callback(f"已抓取 {len(all_reviews)} 条评论")
                last_logged_count = len(all_reviews)
            
            if len(all_reviews) >= max_reviews or time.time() - start_time > max_time:
                break
            
            if len(all_reviews) == last_review_count:
                no_new_reviews_count += 1
            else:
                no_new_reviews_count = 0
            
            if no_new_reviews_count >= 5:
                break
            
            last_review_count = len(all_reviews)
            
            time.sleep(random.uniform(0, 2))

        if not all_reviews:
            print("未能抓取到任何评论")
            if log_callback:
                log_callback("未能抓取到任何评论")
            return None, None

        game_name = driver.find_element(By.CLASS_NAME, "apphub_AppName").text.strip()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"{game_name}_{game_id}_{timestamp}.json"
        json_path = os.path.join("output", json_filename)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(all_reviews, f, ensure_ascii=False, indent=4)
        print(f"JSON文件已保存: {json_path}")

        excel_filename = f"{game_name}_{game_id}_{timestamp}.xlsx"
        excel_path = os.path.join("output", excel_filename)
        df = pd.DataFrame(all_reviews)
        df.to_excel(excel_path, index=False, engine='openpyxl')
        print(f"Excel文件已保存: {excel_path}")
        
        print(f"抓取完成，共 {len(all_reviews)} 条评论")
        print(f"JSON文件已保存: {json_path}")
        print(f"Excel文件已保存: {excel_path}")
        
        if log_callback:
            log_callback(f"抓取完成，共 {len(all_reviews)} 条评论")
            log_callback(f"JSON文件已保存: {json_path}")
            log_callback(f"Excel文件已保存: {excel_path}")
        
        return json_path, excel_path
        
    except Exception as e:
        error_msg = f"抓取过程中出现严重错误：{str(e)}"
        print(error_msg)
        if log_callback:
            log_callback(error_msg, True)
        raise
    finally:
        driver.quit()

    return None, None