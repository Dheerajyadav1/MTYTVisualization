import sys
import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure stdout encoding for special characters
sys.stdout.reconfigure(encoding='utf-8')

# Step 1: Initialize WebDriver
driver = webdriver.Chrome()
driver.get('https://www.youtube.com/@MohitTyagi/videos') # Replace with the url of vieos page of youtube channel you want to scrape
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

# Step 2: Scroll the page (currently 0 times)
body = driver.find_element(By.TAG_NAME, 'body')
for _ in tqdm(range(200)): # Adjust the number of scrolls as needed
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)

# Step 3: Scrape video list
soup = BeautifulSoup(driver.page_source, 'html.parser')
data = []
scrapped = soup.find_all('ytd-rich-item-renderer')

# Extracting video details from videos page
for sp in scrapped:
    title = sp.find('a', class_='yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media').get('title')
    video_length = sp.find('div', class_='badge-shape-wiz__text').text if sp.find('div', class_='badge-shape-wiz__text') else 'N/A'
    video_link = 'https://www.youtube.com' + sp.find('a', class_='yt-simple-endpoint').get('href')
    data.append([title, video_length, video_link])

df = pd.DataFrame(data, columns=['Title', 'Video_length', 'Video_link'])
df.to_csv('youtube_data.csv', index=False) # Save the initial data with required name
print(df)

# Step 4: Scrape individual video details
extra_data = []

def scrape_video_details(url):
    retries = 3
    for attempt in range(retries):
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            title = soup.find('yt-formatted-string', class_='style-scope ytd-watch-metadata').text.strip()
        except:
            title = None

        try:
            like_btn = soup.find('button', class_='yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading yt-spec-button-shape-next--segmented-start yt-spec-button-shape-next--enable-backdrop-filter-experiment')
            like_string = like_btn.get('aria-label') if like_btn else None
            likes = like_string.split()[5] if like_string else None
        except:
            likes = None

        try:
            show_more_button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//tp-yt-paper-button[@id='expand']"))
            )
            driver.execute_script("arguments[0].click();", show_more_button)
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            view_elements = soup.find_all('span', class_='style-scope yt-formatted-string bold')
            views = view_elements[0].text.strip().split()[0] if len(view_elements) > 0 else None
            publish_date = view_elements[2].text.strip() if len(view_elements) > 2 else None
        except:
            views, publish_date = None, None

        try:
            for _ in range(5):
                driver.execute_script("window.scrollBy(0, document.documentElement.scrollHeight / 5);")
                time.sleep(1)
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, "//h2[@id='count']/yt-formatted-string"))
            )
            comment_section = driver.find_element(By.XPATH, "//h2[@id='count']/yt-formatted-string")
            comments = comment_section.text.split()[0]
        except:
            comments = None

        # If all fields are collected, return them
        if all([title, likes, views, publish_date, comments]):
            return [title, likes, views, publish_date, comments]

        time.sleep(2)  # Retry delay

    # If after retries not all values are collected, fill missing with N/A
    return [
        title if title else 'N/A',
        likes if likes else 'N/A',
        views if views else 'N/A',
        publish_date if publish_date else 'N/A',
        comments if comments else 'N/A'
    ]

for link in tqdm(df['Video_link']):
    extra_data.append(scrape_video_details(link))

extra_df = pd.DataFrame(extra_data, columns=['Title', 'Likes', 'Views', 'Publish_date', 'Comments'])

# Merge on Title (assuming titles are unique)
final_df = pd.merge(df, extra_df, on='Title', how='left')
final_df.to_csv('youtube_final_data.csv', index=False) # Save the final data with required name
print(final_df)

# Step 5: Close driver
driver.quit()
