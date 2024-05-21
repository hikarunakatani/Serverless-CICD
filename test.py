import pytest
import json

# Import your Lambda functions
from hello import handler as hello_handler
from users import handler as users_handler


# Mock the DynamoDB client
@pytest.fixture
def mock_dynamodb_client():
    return MagicMock()


# Test the hello function
def test_hello_handler():
    event = {}
    context = {}
    response = hello_handler(event, context)
    assert response["statusCode"] == 200
    assert response["body"] == json.dumps({"message": "Hello, world!"})


# Test the create_user function
def test_create_user_handler(mock_dynamodb_client):
    event = {"body": json.dumps({"id": "123", "name": "John Doe"})}
    context = {}

    # Patch the DynamoDB client with the mock
    users_handler.dynamodb = mock_dynamodb_client

    response = users_handler(event, context)
    assert response["statusCode"] == 201
    assert response["body"] == json.dumps({"message": "User created successfully"})

    # Verify that the DynamoDB client was called with the correct parameters
    mock_dynamodb_client.put_item.assert_called_once_with(
        TableName="users-table",
        Item={
            "id": {"S": "123"},
            "name": {"S": "John Doe"},
        },
    )
