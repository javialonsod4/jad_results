from boto3 import Session

session = Session()

def down(bucket_name, bucket_path, dest_path):
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.download_file(bucket_path, dest_path)

    print(f'{bucket_name} downloaded in {dest_path}')

if __name__ == '__main__':
    bucket_name = 'jad-f-results-bucket'
    bucket_path = 'results.csv'
    dest_path = 'data'
    down(bucket_name, bucket_path, dest_path)
