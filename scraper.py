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

def scrape_steam_reviews(game_id, progress_callback=None, log_callback=None, max_reviews=1000000, max_time=3600, stop_check=None):
    print(f"开始抓取游戏ID: {game_id}")
    if log_callback:
        log_callback(f"开始抓取游戏ID: {game_id}")
    
    url = f"https://steamcommunity.com/app/{game_id}/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=all"
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 在服务器上运行时使用无头模式
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(url)
    
    all_reviews = []
    start_time = time.time()
    last_review_count = 0
    no_new_reviews_count = 0
    
    try:
        while True:
            if stop_check and stop_check():
                print("抓取任务被手动停止")
                if log_callback:
                    log_callback("抓取任务被手动停止")
                break
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            wait_time = random.uniform(3, 5)
            time.sleep(wait_time)
            
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "apphub_Card"))
                )
            except:
                print("无法加载更多评论，可能已到达底部")
                if log_callback:
                    log_callback("无法加载更多评论，可能已到达底部")
                break
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            reviews = soup.find_all("div", class_="apphub_Card")
            
            for review in reviews[last_review_count:]:
                author = review.find("div", class_="apphub_CardContentAuthorName")
                content = review.find("div", class_="apphub_CardTextContent")
                date = review.find("div", class_="date_posted")
                
                if author and content and date:
                    all_reviews.append({
                        "author": author.text.strip(),
                        "content": content.text.strip(),
                        "date": date.text.strip()
                    })
            
            print(f"已抓取 {len(all_reviews)} 条评论")
            if log_callback:
                log_callback(f"已抓取 {len(all_reviews)} 条评论")
            
            if progress_callback:
                progress_callback(len(all_reviews), max_reviews)
            
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

        game_name = soup.find("div", class_="apphub_AppName")
        game_name = game_name.text.strip() if game_name else f"Unknown_Game_{game_id}"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"output/{game_name}_{game_id}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(all_reviews, f, ensure_ascii=False, indent=4)

        df = pd.DataFrame(all_reviews)
        excel_filename = f"output/{game_name}_{game_id}_{timestamp}.xlsx"
        df.to_excel(excel_filename, index=False)

        print(f"抓取完成，共 {len(all_reviews)} 条评论")
        print(f"JSON文件已保存: {json_filename}")
        print(f"Excel文件已保存: {excel_filename}")
        
        if log_callback:
            log_callback(f"抓取完成，共 {len(all_reviews)} 条评论")
            log_callback(f"JSON文件已保存: {json_filename}")
            log_callback(f"Excel文件已保存: {excel_filename}")
        
        return json_filename, excel_filename
        
    except Exception as e:
        error_msg = f"抓取过程中出现严重错误：{str(e)}"
        print(error_msg)
        if log_callback:
            log_callback(error_msg)
        raise
    finally:
        driver.quit()

    return None, None