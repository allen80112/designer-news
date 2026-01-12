import feedparser
import json
import random
from datetime import datetime

# 定義 7 大分類及其對應的 3 個以上權威來源
RSS_FEEDS = {
    "建築": [
        "https://www.archdaily.com/feed",
        "https://www.dezeen.com/architecture/feed/",
        "https://www.architecturalrecord.com/rss/articles"
    ],
    "工業設計": [
        "https://www.core77.com/blog/rss",
        "https://design-milk.com/category/design/feed/",
        "https://www.yankodesign.com/feed/"
    ],
    "互動設計": [
        "https://uxdesign.cc/feed",
        "https://www.smashingmagazine.com/feed/",
        "https://uxmagazine.com/feed/"
    ],
    "藝術": [
        "https://www.designboom.com/art/feed/",
        "https://www.thisiscolossal.com/feed/",
        "https://www.juxtapoz.com/feed/"
    ],
    "平面設計": [
        "https://www.creativebloq.com/feed",
        "https://www.itsnicethat.com/rss",
        "https://www.printmag.com/feed/"
    ],
    "攝影": [
        "https://petapixel.com/feed/",
        "https://www.dpreview.com/index.xml",
        "https://www.lensculture.com/feed"
    ],
    "科技": [
        "https://www.theverge.com/rss/index.xml",
        "https://www.wired.com/feed/rss",
        "https://techcrunch.com/feed/"
    ]
}

def scrape_news():
    all_news = []
    
    for category, urls in RSS_FEEDS.items():
        print(f"📡 正在抓取分類：[{category}]")
        for url in urls:
            try:
                feed = feedparser.parse(url)
                # 每個網站取前 4 則最新的文章
                for entry in feed.entries[:4]:
                    # 抓取圖片邏輯
                    img_url = ""
                    if 'media_content' in entry:
                        img_url = entry.media_content[0]['url']
                    elif 'enclosures' in entry and len(entry.enclosures) > 0:
                        img_url = entry.enclosures[0].href
                    
                    all_news.append({
                        "category": category,
                        "title": entry.title,
                        "link": entry.link,
                        "summary": entry.get("summary", "")[:100].strip() + "...",
                        "source": feed.feed.title if 'title' in feed.feed else "權威來源",
                        "image": img_url,
                        "date": entry.get("published", "")
                    })
            except Exception as e:
                print(f"❌ 無法讀取 {url}: {e}")

    # 打亂順序，讓不同分類混合在一起，增加閱讀樂趣
    random.shuffle(all_news)
    
    # 儲存結果
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=4)
    print(f"✅ 抓取完成！共計 {len(all_news)} 則新聞。")

if __name__ == "__main__":
    scrape_news()
