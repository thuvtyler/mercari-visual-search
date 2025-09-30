# Mercari Visual Fit Search
- This project is a full-stack visual similarity search tool for second-hand Japanese fashion on Mercari Japan. You upload a fit pic, and the app finds visually similar clothing items using CLIP embeddings.

## Features
- Upload an image and receive visually similar Mercari listings
- Uses OpenAI’s CLIP to calculate similarity between user image and Mercari listings
- Scrapes latest listings from Mercari’s LAD MUSICIAN brand page
- Automatically downloads and saves new listing images
- Auto-generates and updates CLIP image embeddings on scrape
- Skips duplicates across multiple runs
- UI built with React + Tailwind styled to feel like SSENSE
- Backend powered by Flask, Python, and Playwright

![App Preview](./preview.png)

## Docker quickstart

You can ship the entire stack as a single Docker image that builds the React frontend, installs the Python/Playwright dependencies, and optionally refreshes the Mercari dataset on startup.

1. **Build the image**
   ```bash
   docker build -t mercari-visual-search .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 mercari-visual-search
   ```
   On first launch the container checks for `mercari_listings.json` and `clip_embeddings.npz`. If they are missing it automatically runs `python run_pipeline.py` inside the container to scrape listings, download images, and regenerate CLIP embeddings before starting the Flask server.

3. **Open the app**
   Visit [http://localhost:5000](http://localhost:5000) in your browser. The Flask backend serves both the API and the built frontend.

### Optional runtime controls

- Skip the pipeline on startup (useful when you mount pre-generated artifacts):
  ```bash
  docker run -p 5000:5000 \
    -e RUN_PIPELINE=never \
    -v $(pwd)/mercari_listings.json:/app/mercari_listings.json \
    -v $(pwd)/clip_embeddings.npz:/app/clip_embeddings.npz \
    -v $(pwd)/images:/app/images \
    mercari-visual-search
  ```
  Ensure the mounted files/directories exist on the host before starting the container.

- Force a fresh scrape every time:
  ```bash
  docker run -p 5000:5000 -e RUN_PIPELINE=always mercari-visual-search
  ```

The container exposes port `5000` and respects the `FLASK_RUN_HOST`, `FLASK_RUN_PORT`, and `FLASK_DEBUG` environment variables if you need to override them.
