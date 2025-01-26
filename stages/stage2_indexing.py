from elasticsearch import Elasticsearch
import hashlib
import os

def index_metadata(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File {image_path} not found.")

    print("Indexing disk image metadata...")

    # Connect to Elasticsearch
    es = Elasticsearch("http://localhost:9200")

    # Calculate hash
    with open(image_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    # Prepare metadata
    metadata = {
        "file_name": os.path.basename(image_path),
        "file_size": os.path.getsize(image_path),
        "file_hash": file_hash,
    }

    # Index metadata
    es.index(index="disk-images", document=metadata)
    print(f"Metadata for {image_path} indexed successfully!")
