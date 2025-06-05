import json
import os
import requests

def download_mercari_images(json_path="mercari_listings.json", output_folder="images"):
    # Load the Mercari listing data
    with open(json_path, "r", encoding="utf-8") as f:
        listings = json.load(f)

    # Make sure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Loop through each listing
    for item in listings:
        item_id = item["link"].split("/")[-1]  # Extract the item ID from the URL
        image_url = item.get("image_url") or item.get("image")
        if image_url and not image_url.startswith("http"):
            print(f"Already have local image for {item_id}: {image_url}")
            continue
        filename = f"{output_folder}/{item_id}.jpg"

        # Skip if already downloaded
        if os.path.exists(filename):
            print(f"Already downloaded: {filename}")
            continue

        # Download and save the image
        try:
            response = requests.get(image_url, timeout=10)
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Failed to download {image_url}: {e}")

# Call the function when this script is run directly
if __name__ == "__main__":
    download_mercari_images()
