import feedparser
import json
import random
import re
from bs4 import BeautifulSoup  # 需安裝此套件
from datetime import datetime

RSS_FEEDS = {
    "建築": ["https://www.archdaily.com/feed", "https://www.dezeen.com/architecture/feed/"],
    "工業設計": ["https://www.core77.com/blog/rss", "https://www.yankodesign.com/feed/"],
    "互動設計": ["https://uxdesign.cc/feed", "https://www.smashingmagazine.com/feed/"],
    "藝術": ["https://www.designboom.com/art/feed/", "https://www.thisiscolossal.com/feed/"],
    "平面設計": ["https://www.creativebloq.com/feed", "https://www.itsnicethat.com/rss"],
    "攝影": ["https://petapixel.com/feed/", "https://www.dpreview.com/index.xml"],
    "科技": ["https://www.theverge.com/rss/index.xml", "https://www.wired.com/feed/rss"]
}

def extract_image(entry):
    """多重機制抓取圖片連結"""
    # 1. 嘗試從標準媒體標籤找
    if 'media_content' in entry:
        return entry.media_content[0]['url']
    if 'enclosures' in entry and len(entry.enclosures) > 0:
        return entry.enclosures[0].href
    
    # 2. 嘗試從內文 (summary 或 content) 抓取 <img> 標籤
    content = ""
    if 'summary' in entry: content += entry.summary
    if 'content' in entry: content += entry.content[0].value
    
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        img = soup.find('img')
        if img and img.get('src'):
            return img['src']
            
    return "" # 真的沒圖才回傳空值

def scrape_news():
    all_news = []
    for category, urls in RSS_FEEDS.items():
        for url in urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:5]:
                    img_url = extract_image(entry)
                    
                    # 清理摘要內容，移除 HTML 標籤
                    summary_text = BeautifulSoup(entry.get("summary", ""), "html.parser").get_text()
                    
                    all_news.append({
                        "category": category,
                        "title": entry.title,
                        "link": entry.link,
                        "summary": summary_text[:100].strip() + "...",
                        "source": feed.feed.title if 'title' in feed.feed else "設計媒體",
                        "image": img_url
                    })
            except Exception as e:
                print(f"Error scraping {url}: {e}")

    random.shuffle(all_news)
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scrape_news()
