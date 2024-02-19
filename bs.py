import os
import csv
import requests
from PIL import Image
from io import BytesIO
from multiprocessing import Pool

def download_and_process_image(row):
    id, emotion, url, disagrees, agrees = row
    save_path_tmp = f'/tmp/polarity_image/{id}.jpg'
    save_path_final = f'data/polarity_image/{id}.jpg'

    try:
        # Download image to /tmp
        img_response = requests.get(url)
        img_response.raise_for_status()

        with open(save_path_tmp, 'wb') as img_file:
            img_file.write(img_response.content)

        # Convert image to RGB using PIL
        pil_image = Image.open(save_path_tmp)
        pil_image_rgb = pil_image.convert('RGB')

        # Save the final image to data/polarity_image
        pil_image_rgb.save(save_path_final, format='JPEG', quality=90)
        print(f"Image {id} saved to {save_path_final}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image {id}: {e}")

if __name__ == '__main__':
    # Ensure the directories exist
    tmp_dir = '/tmp/polarity_image'
    final_dir = 'data/polarity_image'

    os.makedirs(tmp_dir, exist_ok=True)
    os.makedirs(final_dir, exist_ok=True)

    # Read CSV file
    with open('data/visual_sentiment_cat.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)  # Skip header
        rows = list(reader)

    # Use multiprocessing to download and process images in parallel
    with Pool(processes=os.cpu_count()) as pool:
        pool.map(download_and_process_image, rows)
