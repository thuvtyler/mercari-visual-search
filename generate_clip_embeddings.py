import os
import torch
import clip
from PIL import Image
import numpy as np

def generate_clip_embeddings(image_folder="images", output_file="clip_embeddings.npz"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)

    embeddings = []
    filenames = []

    for filename in os.listdir(image_folder):
        if not filename.endswith(".jpg"):
            continue

        image_path = os.path.join(image_folder, filename)

        try:
            image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
            with torch.no_grad():
                image_features = model.encode_image(image)
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)
                embeddings.append(image_features.cpu().numpy())
                filenames.append(filename)
            print(f"Encoded: {filename}")
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

    # Save embeddings and filenames to disk
    np.savez(output_file, embeddings=np.vstack(embeddings), filenames=np.array(filenames))
    print(f"Saved {len(embeddings)} embeddings to {output_file}")

if __name__ == "__main__":
    generate_clip_embeddings()