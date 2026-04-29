import boto3

def load_data_from_s3(bucket_name, prefix, local_path):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            local_file_path = f"{local_path}/{key.split('/')[-1]}"
            s3.download_file(bucket_name, key, local_file_path)
            print(f"Downloaded {key} to {local_file_path}")