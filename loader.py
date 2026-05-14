import boto3
import os
    
DATA_BUCKET_NAME = os.getenv("DATA_BUCKET_NAME")

def load_data_from_s3(bucket_name, prefix, local_path):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    normalized_prefix = prefix.rstrip('/') + '/' if prefix and not prefix.endswith('/') else prefix

    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            relative_key = key[len(normalized_prefix):] if normalized_prefix and key.startswith(normalized_prefix) else key
            local_file_path = os.path.join(local_path, relative_key)
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            s3.download_file(bucket_name, key, local_file_path)
            print(f"Downloaded {key} to {local_file_path}")

if __name__ == "__main__":
    data_dir = 'data'
    data_prefix = 'cats-and-dogs-image-classification/'

    if not DATA_BUCKET_NAME:
        raise ValueError("DATA_BUCKET_NAME environment variable is not set. Please set it to the name of your S3 bucket containing the data.")

    # Download data from S3 (if needed)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        load_data_from_s3(bucket_name=DATA_BUCKET_NAME, prefix=data_prefix, local_path=data_dir)
    else:
        print(f"Data directory '{data_dir}' already exists. Skipping download.")
