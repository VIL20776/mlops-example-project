import boto3
import os

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