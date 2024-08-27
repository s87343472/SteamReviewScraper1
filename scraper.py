import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_steam_reviews(game_id, max_reviews=50000, max_scroll_attempts=100, stop_flag_callback=None, log_callback=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 设置无头模式
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://steamcommunity.com/app/{game_id}/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=all#"
    log_callback(f"打开页面: {url}")
    driver.get(url)

    try:
        view_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'浏览社区中心')]"))
        )
        view_page_button.click()
        log_callback("通过点击浏览社区中心按钮绕过成人内容验证")
    except Exception as e:
        log_callback(f"无需PG18验证，或验证已自动跳过: {e}")

    time.sleep(5)

    total_reviews = []
    last_review_count = 0
    scroll_attempts = 0

    while len(total_reviews) < max_reviews and scroll_attempts < max_scroll_attempts:
        if stop_flag_callback and stop_flag_callback():
            log_callback("停止抓取指令收到，停止抓取...")
            break

        log_callback(f"滚动页面以加载更多评论... (已抓取 {len(total_reviews)} 条评论)")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        wait_time = random.uniform(3, 7)  # 随机等待时间
        time.sleep(wait_time)

        reviews = driver.find_elements(By.CLASS_NAME, "apphub_Card")
        
        if len(reviews) > last_review_count:
            for review in reviews[last_review_count:]:
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

                    total_reviews.append({
                        "username": username,
                        "playtime": playtime,
                        "content": content,
                        "recommended": recommended,
                        "owned_products": owned_products,
                        "found_helpful": found_helpful
                    })
                except Exception as e:
                    log_callback(f"解析评论时出错: {e}")

            last_review_count = len(reviews)
        else:
            scroll_attempts += 1
            log_callback(f"未加载到新评论，尝试滚动 {scroll_attempts}/{max_scroll_attempts} 次")

    driver.quit()
    return total_reviews