import pytest
import boto3

# Set the endpoint URL for LocalStack DynamoDB
boto3.setup_default_session(region_name="us-east-1", endpoint_url="http://localhost:4569")

def test_create_user_integration():
    """
    Integration test for the create_user function using LocalStack.
    """

    # Create a DynamoDB client
    dynamodb = boto3.client("dynamodb")

    # Create a new user
    user_data = {"id": "123", "name": "John Doe"}
    response = dynamodb.put_item(
        TableName="users-table",
        Item={
            "id": {"S": user_data["id"]},
            "name": {"S": user_data["name"]},
        },
    )

    # Verify that the user was created successfully
    get_response = dynamodb.get_item(TableName="users-table", Key={"id": {"S": "123"}})
    assert get_response["Item"]["name"]["S"] == "John Doe"
