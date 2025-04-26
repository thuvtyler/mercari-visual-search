import numpy as np
import torch
import clip
from PIL import Image
import json

def find_similar_items(query_image_path="query.jpg", embedding_file="clip_embeddings.npz", listings_file="mercari_listings.json", top_k=50, return_results=False):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)

    # Load embeddings
    data = np.load(embedding_file)
    embeddings = data["embeddings"]
    filenames = data["filenames"]

    # Load listing metadata
    with open(listings_file, "r", encoding="utf-8") as f:
        listings = json.load(f)
    listings_dict = {item["link"].split("/")[-1] + ".jpg": item for item in listings}

    # Encode query image
    query_image = preprocess(Image.open(query_image_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        query_embedding = model.encode_image(query_image)
        query_embedding = query_embedding / query_embedding.norm(dim=-1, keepdim=True)
        query_embedding = query_embedding.cpu().numpy()

    # Cosine similarity
    similarities = embeddings @ query_embedding.T
    similarities = similarities.squeeze()

    # Top matches
    top_indices = similarities.argsort()[::-1][:top_k]

    results = []
    for i in top_indices:
        filename = filenames[i]
        sim_score = float(similarities[i])
        listing = listings_dict.get(filename)

        if listing:
            results.append({
                "filename": filename,
                "similarity": round(sim_score, 4),
                "title": listing["title"],
                "price": listing["price"],
                "link": listing["link"].replace("https://www.mercari.com", "https://jp.mercari.com")

            })

    if return_results:
        return results
    else:
        print("\nTop similar items:")
        for r in results:
            print(f"{r['filename']} - {r['similarity']} - {r['title']}")

if __name__ == "__main__":
    find_similar_items()
