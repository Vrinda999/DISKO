from os import close
from elasticsearch import Elasticsearch
import hashlib
import os
from tqdm import tqdm

def index_metadata(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File {image_path} not found.")

    print("Indexing disk image metadata...")

    # Connect to Elasticsearch
    es = Elasticsearch("http://localhost:9200")

    # Calculate hash
    # with open(image_path, "rb") as f:
    #     file_hash = hashlib.sha256(f.read()).hexdigest()

    file_size = os.path.getsize(image_path)
    file_hash = hashlib.sha256()
    with open(image_path, "rb") as f, tqdm(
        total = file_size, unit = "B", unit_scale = True, desc = "Hashing"
    ) as progress:
        while chunk := f.read(15360):      # read in 15MB chunks
            file_hash.update(chunk)
            progress.update(len(chunk))  # Update progress bar

        file_hash = file_hash.hexdigest()
    f.close()


    # Prepare metadata
    metadata = {
        "file_name": os.path.basename(image_path),
        "file_size": os.path.getsize(image_path),
        "file_hash": file_hash,
    }


    # Index metadata
    try:
        es.index(index="disk-images", document=metadata)
        print(f"Metadata for {image_path} indexed successfully!")
    except Exception as e:
        print(f"Error indexing metadata: {e}")

img = input("Enter Image Path (../op.dd): ")
index_metadata(img)