import os
import json
import hashlib
import requests
from time import sleep
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

BASE_URL = "https://jp.mercari.com"
BRAND_URL = "https://jp.mercari.com/search?brand_id=1269&sort=created_time&order=desc"
OUTPUT_JSON = "mercari_listings.json"
IMAGES_DIR = "images"
SEEN_IDS = set()

# Load previously scraped IDs
if os.path.exists(OUTPUT_JSON):
    with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
        for item in json.load(f):
            SEEN_IDS.add(item["id"])

def download_image(img_url, filename):
    try:
        r = requests.get(img_url, timeout=10)
        r.raise_for_status()
        with open(os.path.join(IMAGES_DIR, filename), "wb") as f:
            f.write(r.content)
    except Exception as e:
        print(f"[!] Failed to download {img_url}: {e}")

def scrape_mercari_pages(pages=10):
    os.makedirs(IMAGES_DIR, exist_ok=True)
    results = []

    # Load previous results
    if os.path.exists(OUTPUT_JSON):
        with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
            results = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(locale="ja-JP")
        page = context.new_page()

        for page_num in range(pages):
            url = BRAND_URL + (f"&page_token=v1%3A{page_num}" if page_num > 0 else "")
            print(f"Scraping page {page_num+1}: {url}")
            page.goto(url)

            try:
                page.wait_for_selector("a[data-testid='thumbnail-link']", timeout=10000)
            except:
                print(f"[!] Listings not found on page {page_num+1}")
                continue

            soup = BeautifulSoup(page.content(), "html.parser")
            cards = soup.select("a[data-testid='thumbnail-link']")

            if not cards:
                print(f"[!] No cards found on page {page_num+1}")
                continue

            for card in cards:
                href = card.get("href")
                if not href or not href.startswith("/item/"):
                    continue

                listing_id = href.split("/")[-1]
                if listing_id in SEEN_IDS:
                    continue

                img = card.find("img")
                title = img.get("alt", "").strip() if img else "No title"
                img_url = img.get("src") if img else None

                # Scrape price from sibling <p> with ¥ in text
                parent_div = card.find_parent("div", class_=lambda x: x and "mer-item-thumbnail" in x)
                price_tag = parent_div.find(string=lambda x: x and "¥" in x) if parent_div else None
                price = price_tag.strip() if price_tag else "N/A"

                filename = f"{listing_id}.jpg"
                if img_url:
                    download_image(img_url, filename)

                result = {
                    "id": listing_id,
                    "title": title,
                    "link": BASE_URL + href,
                    "price": price,
                    "image": filename
                }
                results.append(result)
                SEEN_IDS.add(listing_id)

            sleep(1.5)

        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        browser.close()
        print(f"✅ Scraping done. Total listings: {len(results)}")

if __name__ == "__main__":
    scrape_mercari_pages(10)
