import time
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 引入一个全局变量来控制抓取的终止
is_scraping = True

def stop_scraping():
    global is_scraping
    is_scraping = False

def scrape_steam_reviews(game_id, max_reviews=50000, max_scroll_attempts=100):
    global is_scraping
    is_scraping = True  # 每次开始抓取时重置标志位

    print(f"开始抓取游戏ID为 {game_id} 的评论")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://steamcommunity.com/app/{game_id}/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=all#"
    print(f"打开页面: {url}")
    driver.get(url)

    # 处理PG18验证
    try:
        view_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'浏览社区中心')]"))
        )
        view_page_button.click()
        print("通过点击浏览社区中心按钮绕过成人内容验证")
    except Exception as e:
        print(f"无需PG18验证，或验证已自动跳过: {e}")

    time.sleep(5)

    total_reviews = []
    last_review_count = 0
    scroll_attempts = 0

    while len(total_reviews) < max_reviews and scroll_attempts < max_scroll_attempts and is_scraping:
        print(f"滚动页面以加载更多评论... (已抓取 {len(total_reviews)} 条评论)")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 增加随机等待时间
        wait_time = random.uniform(3, 7)  # 随机等待3到7秒
        time.sleep(wait_time)

        reviews = driver.find_elements(By.CLASS_NAME, "apphub_Card")
        
        if len(reviews) > last_review_count:
            for review in reviews[last_review_count:]:
                if not is_scraping:  # 检查是否需要停止抓取
                    break
                try:
                    username = review.find_element(By.CLASS_NAME, "apphub_CardContentAuthorName").text
                    playtime = review.find_element(By.CLASS_NAME, "hours").text
                    content = review.find_element(By.CLASS_NAME, "apphub_CardTextContent").text
                    recommended = "推荐" if "Recommended" in review.find_element(By.CLASS_NAME, "title").text else "不推荐"
                    try:
                        owned_products = review.find_element(By.CLASS_NAME, "apphub_CardContentMoreLink").text
                    except:
                        owned_products = ""

                    try:
                        found_helpful = review.find_element(By.CLASS_NAME, "found_helpful").text
                    except:
                        found_helpful = ""

                    try:
                        review_date = review.find_element(By.CLASS_NAME, "date_posted").text
                    except:
                        review_date = ""

                    total_reviews.append({
                        "username": username,
                        "playtime": playtime,
                        "content": content,
                        "recommended": recommended,
                        "owned_products": owned_products,
                        "found_helpful": found_helpful,
                        "review_date": review_date
                    })
                except Exception as e:
                    print(f"解析评论时出错: {e}")

            last_review_count = len(reviews)
        else:
            scroll_attempts += 1
            print(f"未加载到新评论，尝试滚动 {scroll_attempts}/{max_scroll_attempts} 次")

            # 检查页面底部是否存在“没有更多内容”提示
            try:
                end_of_page = driver.find_element(By.XPATH, "//div[contains(text(),'没有更多内容')]")
                if end_of_page:
                    print("检测到没有更多内容，停止滚动。")
                    break
            except:
                pass

        if len(total_reviews) >= max_reviews:
            print("已达到最大抓取评论数。")
            break

    # 保存评论数据
    json_file = f"{game_id}_reviews.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(total_reviews, f, ensure_ascii=False, indent=4)
    
    print(f"评论已保存到 {json_file}")
    print(f"抓取完成，总共抓取了 {len(total_reviews)} 条评论。")

    driver.quit()
    return json_file