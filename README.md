# 📺 YouTube Channel Video Scraper with Power BI Visualization

This project is a Python-based YouTube scraper that collects detailed video-level data from a public YouTube channel. It uses **Selenium** and **BeautifulSoup** to extract information like video title, link, length, likes, views, comments, and published date.

Later, this scraped data can be used to visualize insights using **Power BI**.

---

## 🚀 Features

- Scrapes videos from a specific YouTube channel's **Videos** tab
- Scrolls automatically to load more videos
- Extracts key metadata for each video:
  - Title
  - Video length
  - Video link
  - Likes
  - Views
  - Publish date
  - Comment count
- Exports data to two CSV files
- Ready for Power BI visualizations

---

## 🧾 Files in this Repository

| File Name              | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `youtube_scraper.py`   | Python script that performs scraping using Selenium and BeautifulSoup       |
| `youtube_data.csv`     | Raw scraped video data (titles, lengths, links)                             |
| `youtube_final_data.csv`| Enriched data with likes, views, comments, publish date                    |
| `requirements.txt`     | List of Python dependencies for this project                                |
| `powerbi_dashboard.pbix` | Power BI file (to be added by you) containing visualization of the data   |
| `README.md`            | Documentation and instructions                                              |

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/youtube-scraper-powerbi.git
cd youtube-scraper-powerbi
