import boto3  
from datetime import datetime  
import time  
import json  
  
  
class _CloudWatch:  
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_session_token):  
        self.client = boto3.client(  
            'logs',  
            aws_access_key_id=aws_access_key_id,  
            aws_secret_access_key=aws_secret_access_key,  
            aws_session_token=aws_session_token  
        )  
  
    def run_query(self, log_group: str, query: str, start_time: datetime, end_time: datetime, export_to_file=False):  
  
        start_query_response = self.client.start_query(  
            logGroupName=log_group,  
            startTime=int(start_time.timestamp()),  
            endTime=int(end_time.timestamp()),  
            queryString=query  
        )  
  
        query_id = start_query_response['queryId']  
        response = None  
  
        while response is None or response['status'] == 'Running':  
            response = self.client.get_query_results(  
                queryId=query_id  
            )  
            time.sleep(1)  
            print(datetime.now(), '- Waiting for query to complete')  
  
        if export_to_file:  
            with open('CloudWatch.log', 'w+') as file_output:  
                file_output.write(json.dumps(response, indent=4))  
  
        return response  
  
  
class _S3:  
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_session_token):  
        self.client = boto3.client(  
            's3',  
            aws_access_key_id=aws_access_key_id,  
            aws_secret_access_key=aws_secret_access_key,  
            aws_session_token=aws_session_token  
        )  
  
    def list_s3_buckets(self) -> list:  
        return [bucket.name for bucket in self.client.list_buckets()]  
  
    def list_s3_bucket_files(self, bucket_name: str, prefix: str = '') -> list:  
        response = dict(self.client.list_objects_v2(  
            Bucket=bucket_name  
        ))  
        try:  
            return [file['Key'] for file in response['Contents']]  
        except KeyError:  
            return [f'No objects found in {bucket_name}']  
  
  
class AWS:  
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_session_token):  
        self.cloudwatch = _CloudWatch(  
            aws_access_key_id,  
            aws_secret_access_key,  
            aws_session_token  
        )  
        self.s3 = _S3(  
            aws_access_key_id,  
            aws_secret_access_key,  
            aws_session_token  
        )