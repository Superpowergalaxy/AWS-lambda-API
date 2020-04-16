import json
import os
import boto3
import csv
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def upload_to_dynamodb(NBA_database, csvlines, header):
    for line in csvlines:
        item = {}
        for i in range(len(header) - 1):
            item[header[i+1]] = line[i+1]
        # upload data
        response = NBA_database.put_item(Item = item)
    return response
        
def read_s3_csv(bucket,file_key):
    obj = s3.get_object(Bucket=bucket, Key=file_key)
    data = obj['Body'].read().decode('utf-8').splitlines()
    lines = csv.reader(data)
    headers = next(lines)
    return lines, headers
    
def lambda_handler(event, context):
    # TODO implement
    #get file from s3
    bucket = 'nba-team-match-status'
    file_key = 'nba-prediction.csv'
    csvlines, header = read_s3_csv(bucket,file_key)
    
    # connect to dynamo:
    NBA_database = dynamodb.Table('nba-match')
    # upload function 
    response = upload_to_dynamodb(NBA_database, csvlines,header)

    return{
        'message' : response        
    }  
