from tools.password_verification import hash


def test_create_user(client):
    # Test a successful user creation
    user_data = {
        "name": "amit",
        "email": "amit_1@hcl.com",
        "age": 27,
        "company_id": 52155651,
        "projects_handled": ["vodafone", "airtel", "idea"],
        "phone_number": "8197920447",
    }
    response = client.post(
        "/user/?address=bengalore&married_status=false&password=pass", json=user_data
    )
    assert response.status_code == 201
    res = response.json()
    res.pop("password")
    assert res == {
        **user_data,
        "address": "bengalore",
        "married_status": False,
        # "password": hash("pass"),
    }

    # Test a user creation with invalid age
    user_data = {
        "name": "amit",
        "email": "amit_2@hcl.com",
        "age": 7,
        "company_id": 5215561,
        "projects_handled": ["vodafone", "airtel", "idea"],
        "phone_number": 93,
    }
    response = client.post(
        "/user/?address=bengalore&married_status=true&password=pass", json=user_data
    )
    assert response.status_code == 400

    # Test a user creation with missing required fields
    user_data = {"age": 30, "email": "test@example.com"}
    response = client.post("/user/", json=user_data)
    assert response.status_code == 422


def test_get_users_by_id(client):
    # Create a test user
    test_create_user(client)

    # Test getting an existing user by ID
    response = client.get("/user/1")
    assert response.status_code == 200

    # Test getting a non-existent user by ID
    response = client.get("/user/999")
    assert response.status_code == 400


def test_get_all_users(client):
    # Create a test user
    test_create_user(client)

    # Test getting all users
    response = client.get("/user/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_update_user(client):
    # Create a test user
    test_create_user(client)

    # Test updating an existing user by ID
    user_data = {
        "name": "amit",
        "email": "amit_sahu@hcl.com",
        "age": 27,
        "company_id": 52155651,
        "projects_handled": ["vodafone", "airtel", "idea"],
        "phone_number": 93,
    }
    response = client.put("/user/1", json=user_data)
    assert response.status_code == 200

    # Test updating a non-existent user by ID
    response = client.put("/user/999", json=user_data)
    assert response.status_code == 400


def test_delete_user(client):
    # Create a test user
    test_create_user(client)

    # Test deleting an existing user by ID
    response = client.delete("/user/1")
    assert response.status_code == 200

    # Test deleting a non-existent user by ID
    response = client.delete("/user/999")
    assert response.status_code == 400
