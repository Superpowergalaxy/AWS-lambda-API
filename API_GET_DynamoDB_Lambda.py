import json
import boto3
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    
    # connect to the data base
    NBA_database = dynamodb.Table('nba-match')
    team = event['queryStringParameters']['Team']
    oppt = event['queryStringParameters']['Oppt']
    
    # queue the data base database
    queue_response = NBA_database.get_item(
        Key={
            'Team': team,
            'Oppt':oppt
        }
    )
    
    # create a response
    responseObject = {}
    responseObject['statusCode'] = queue_response['ResponseMetadata']['HTTPStatusCode']
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = queue_response['Item']
	
    return responseObject
