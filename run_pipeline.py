import os
import json
from scrape_mercari import scrape_mercari_pages
from download_mercari_images import download_mercari_images
from generate_clip_embeddings import generate_clip_embeddings

def remove_duplicates(input_file="mercari_listings.json", output_file="mercari_listings.json"):
    print("Removing duplicate listings...")

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    seen_ids = set()
    unique_items = []
    for item in data:
        item_id = item.get("id")
        if item_id and item_id not in seen_ids:
            seen_ids.add(item_id)
            unique_items.append(item)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(unique_items, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(unique_items)} unique items saved.")

def main():
    print("\n🚀 Starting Mercari Visual Search Pipeline")

    # Step 1: Scrape listings
    scrape_mercari_pages(pages=2)

    # Step 2: Remove duplicates
    remove_duplicates()

    # Step 3: Download images
    download_mercari_images("mercari_listings.json")

    # Step 4: Generate CLIP embeddings
    generate_clip_embeddings("images", "clip_embeddings.npz")

    print("\n🎉 Pipeline complete. Ready to search!")

if __name__ == "__main__":
    main()
