from io import StringIO
import boto3

BUCKET_NAME = "arn:aws:s3:::personalization-log"
url = "https://personalization-log.s3.ap-northeast-2.amazonaws.com/20210803_092257.jpg"
s3_address = 's3://personalization-log/dummy.csv'


def upload_csv_file(df, file_name):
    bucket = 'personalization-log'  # already created on S3
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, file_name).put(Body=csv_buffer.getvalue())


