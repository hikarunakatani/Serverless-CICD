import os
import json
import boto3


def handler(event, context):
    """
    A Lambda function that creates a new user in a DynamoDB table.
    """

    # Get the user data from the request body
    user_data = json.loads(event["body"])

    # Create a DynamoDB client
    dynamodb = boto3.client("dynamodb")

    # Insert the user data into the DynamoDB table
    try:
        response = dynamodb.put_item(
            TableName=os.environ["TABLE_NAME"],
            Item={
                "id": {"S": user_data["id"]},
                "name": {"S": user_data["name"]},
                # Add more attributes as needed
            },
        )
    except ClientError as error:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(error)}),
        }

    # Return a success response
    return {
        "statusCode": 201,
        "body": json.dumps({"message": "User created successfully"}),
    }
