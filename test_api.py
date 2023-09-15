import requests
from pprint import pprint

# Replace with your server URL
BASE_URL = "http://web-01.cofucan.tech/api"


# Helper function to print responses with proper formatting
def print_response(response):
    print(f"Status Code: {response.status_code}")
    print("Response:")
    pprint(response.text)
    print()


# Test creating a new user
new_user_data = {
    "name": "Test User",
    "gender": "M",
    "email": "test@example.com",
    "username": "testuser",
    "track_id": 1
}

response = requests.post(f"{BASE_URL}/", json=new_user_data)
count = 0

# Extract the user ID from the response
while response.status_code != 200 and count < 5:
    response = requests.post(f"{BASE_URL}/", json=new_user_data)
    count += 1

print("Create User:")
print_response(response)

created_user = response.json()
user_id = created_user["id"]

# Test getting the user by ID
response = requests.get(f"{BASE_URL}/{user_id}")
print("Get User by ID:")
print_response(response)

# Test updating a user
update_data = {
    "name": "Updated User",
    "email": "updated@example.com",
    "stage": 2
}

response = requests.put(f"{BASE_URL}/{user_id}", json=update_data)
print("Update User:")
print_response(response)

# Test filtering users
filter_criteria = {
    "gender": "M"
}

response = requests.get(f"{BASE_URL}/", json=filter_criteria)
print("Get Users with Filtering Criteria:")
print_response(response)

# Test deleting the user by ID
response = requests.delete(f"{BASE_URL}/{user_id}")
print("Delete User by ID:")
print_response(response)

# print("Failed to create user. Skipping Get and Delete operations.")

# Test getting all users
response = requests.get(f"{BASE_URL}/")
print("Get All Users:")
print_response(response)
