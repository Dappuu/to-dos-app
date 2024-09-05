# To-dos API
To-do app API service for Nashtech's "Python Web Develop with FastAPI" course by Bui Viet Dat - SD5968.

## Running development server

### Requirements

- Python 3.11.9
- Docker

### Setup

1. **Start the PostgreSQL Database Container**:
    Run the following command to start a PostgreSQL container:
    ```bash
    docker run -d --name postgres -e POSTGRES_PASSWORD=230377 -e POSTGRES_DB="to-dos-app" -p 5433:5432 postgres:14
    ```
2. **Install Python Dependencies**: 
    Use pip to install the necessary Python packages: 
    ```bash
    pip install -r requirements.txt
    ```
3. **Run Database Migrations**: Apply the database migrations using Alembic: 
    ```bash
    alembic upgrade head
    ```
4. **Start the API Server**: Run the following command to start the API server with Uvicorn: 
    ```bash
    uvicorn app.main:app --reload
    ``` 
5. **Access the API**:
    - API service: `http://localhost:8000`
    - Swagger documentation: `http://localhost:8000/docs`
## Seed Data

### Company Table
| id | name | description |
|----|------|-------------|
| [UUID] | Example Corp | An example company |

### User Table
| id | email | username | first_name | last_name | hashed_password | is_active | is_admin | company_id |
|----|-------|----------|------------|-----------|-----------------|-----------|----------|------------|
| [UUID] | admin@example.com | admin | Admin | Last_Name | [hashed ADMIN_PASSWORD] | True | True | [company_id] |
| [UUID] | user@example.com | user | User | Last_Name | [hashed USER_PASSWORD] | True | False | [company_id] |

### Task Table
| id | summary | description | status | priority | assigner_id | doer_id |
|----|---------|-------------|--------|----------|-------------|---------|
| [UUID] | Admin task | This is the first task | NEW | 1 | [admin_id] | [admin_id] |
| [UUID] | Admin -> User | This is the first task | NEW | 1 | [admin_id] | [user_id] |
| [UUID] | User -> User | This is the first task | NEW | 1 | [user_id] | [user_id] |

## API Error Response Documentation

This document outlines common error responses that may be encountered when interacting with the API.

### Authentication Errors

#### 1. Invalid Credentials

When a user attempts to access any API endpoint without valid authentication credentials, they will receive the following response:

- **Code**: 401 Unauthorized
- **Content**:
  ```json
  {
    "detail": "Invalid username or password"
  }
  ```

#### 2. Inactive Account

If a user's account has been disabled (i.e., the `is_active` property is set to `false`), attempts to log in will result in the following response:

- **Code**: 403 Forbidden
- **Content**:
  ```json
  {
    "detail": "Inactive Account"
  }
  ```

### 3. Access Denied

Some APIs require an admin privelege. Attempts to use those without permission will result in the following response:

  - **Code**: 401 Unauthorized
  - **Content**: 
  ```json
  {
    "detail": "Unauthorized Access"
  }
  ```

## Auth API documentation

### Login for Access Token

Authenticates the user and returns an access token.

- **URL**: `/token`
- **Method**: `POST`
- **Query Parameters**:
    - `username` (UUID, required, email)
    - `password` (string, required)
- **Success Response**: 
    - Code: 200 OK
    - Content: 
        ```json
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }
        ```
- **Error Response**: 
    - Code: 401 Unauthorized
    - Content: 
        ```json
        {
            "detail": "Incorrect username or password"
        }
        ```
- **Note**:
    - The access token is valid for 10 minutes.
    - Use the access token in the Authorization header for subsequent requests that require authentication.
    - The token type is "bearer", so include it in the Authorization header as: `Authorization: Bearer <access_token>`.

## Company API Documentation

This document outlines the API endpoints for managing company data. All endpoints require admin privileges.

### Base URL

All endpoints are prefixed with `/company`.

### Endpoints

#### 1. Get All Companies

Retrieves a list of companies based on optional filter criteria.

- **URL**: `/`
- **Method**: `GET`
- **Query Parameters**:
  - `company_id` (UUID, optional): Filter by company ID
  - `company_name` (string, optional): Filter by company name
  - `page` (int, default=1): Page number for pagination
  - `size` (int, default=10, max=50): Number of items per page
- **Authentication**: Required (Admin only)
- **Success Response**: 
  - Code: 200 Ok
  - Content: 
    ```json
    [
        {
            "id": "UUID",
            "name": "string",
            "description": "string"
        }
    ]
    ```

#### 2. Get Company by ID

Retrieves details of a specific company.

- **URL**: `/{company_id}`
- **Method**: `GET`
- **URL Parameters**: 
  - `company_id` (UUID, required): ID of the company to retrieve
- **Authentication**: Required (Admin only)
- **Success Response**: 
  - Code: 200 Ok
  - Content: 
    ```json
    {
        "id": "UUID",
        "name": "string",
        "description": "string"
    }
    ```
- **Error Response**: 
  - Code: 404 Not Found
  - Content: `{"detail": "Resource Not Found"}`

#### 3. Create Company

Creates a new company.

- **URL**: `/`
- **Method**: `POST`
- **Authentication**: Required (Admin only)
- **Request Body**: 
  ```json
    {
      "name": "string"
      "description": "string",
    }
    ```
- **Success Response**: 
    - Code: 200 Ok
    - Content: 
    ```json
    {
        "id": "UUID",
        "name": "string",
        "description": "string"
    }
    ```

#### 4. Update Company

Updates an existing company.

- **URL**: `/{company_id}`
- **Method**: `PUT`
- **URL Parameters**: 
  - `company_id` (UUID, required): ID of the company to update
- **Request Body**: 
    ```json
    {
        "name": "string",
        "description": "string"
    }
    ```
- **Authentication**: Required (Admin only)
- **Success Response**: 
    - Code: 201 Created
    - Content: 
    ```json
    {
        "id": "UUID",
        "name": "string",
        "description": "string"
    }
    ```
- **Error Response**: 
  - Code: 404 Not Found
  - Content: `{"detail": "Resource Not Found"}`

#### 5. Delete Company

Deletes a company.

- **URL**: `/{company_id}`
- **Method**: `DELETE`
- **URL Parameters**: 
  - `company_id` (UUID, required): ID of the company to delete
- **Authentication**: Required (Admin only)
- **Success Response**: 
  - Code: 204 No Content
  - Content: None
- **Error Response**: 
  - Code: 404 Not Found
  - Content: `{"detail": "Resource Not Found"}`

## Task API Documentation

This document outlines the API endpoints for managing task data.

### Base URL

All endpoints are prefixed with `/task`.

### Enum

The Task table includes a "status" column that uses an enumeration to represent the current state of a task. The possible status values are defined as follows:
  ```json
  enum STATUS {
      NEW = "N",
      IN_PROGRESS = "IP",
      PENDING = "P",
      ABANDONED = "A",
      DONE = "D"
  }
  ```
Status Descriptions:

- NEW ("N"): The task has been created but work has not yet begun.
- IN_PROGRESS ("IP"): Work on the task is currently underway.
- PENDING ("P"): The task is temporarily on hold or awaiting some external action.
- ABANDONED ("A"): Work on the task has been discontinued before completion.
- DONE ("D"): The task has been completed.

### Endpoints

#### 1. Get Tasks By User ID

Retrieves a list of tasks for a specific user.

- **URL**: `/{user_id}`
- **Method**: `GET`
- **URL Parameters**:
  - `user_id` (UUID, required): ID of the user whose tasks to retrieve
- **Authentication**: Required
- **Success Response**: 
    - Code: 200 Ok
    - Content: 
    ```json
    {
        "id": "UUID",
        "summary": "string",
        "description": "string",
        "status": "STATUS",
        "priority": "integer",
        "assigner_id": "UUID",
        "doer_id": "UUID"
    }
    ```
- **Error Response**: 
  - Code: 404 Not Found
  - Content: `{"detail": "Resource Not Found"}`

#### 2. Create Task

Creates a new task. New task will automatically initialize the "status" with "NEW" value. This endpoint sets the authenticated user as the assigner when creating a task.

- **URL**: `/`
- **Method**: `POST`
- **Request Body**: 
    ```json
    {
        "summary": "string",
        "description": "string",
        "priority": "integer",
        "doer_id": "UUID"
    }
    ```
- **Authentication**: Required
- **Success Response**: 
    - Code: 200 Ok
    - Content: 
    ```json
    {
        "id": "UUID",
        "summary": "string",
        "description": "string",
        "status": "STATUS",
        "priority": "integer",
        "assigner_id": "UUID",
        "doer_id": "UUID"
    }
    ```

#### 3. Update Task

Updates an existing task.

- **URL**: `/{task_id}`
- **Method**: `PUT`
- **URL Parameters**: 
  - `task_id` (UUID, required): ID of the task to update
- **Request Body**: 
    ```json
    {
        "summary": "string",
        "description": "string",
        "status": "string",
        "priority": "integer",
        "doer_id": "UUID"
    }
    ```
- **Authentication**: Required
- **Success Response**: 
    - Code: 201 Created
    - Content: 
    ```json
    {
        "id": "UUID",
        "summary": "string",
        "description": "string",
        "status": "STATUS",
        "priority": "integer",
        "assigner_id": "UUID",
        "doer_id": "UUID"
    }
    ```
- **Error Response**: 
  - Code: 404 Not Found
  - Content: `{"detail": "Resource Not Found"}`

#### 4. Delete Task

Deletes a task.

- **URL**: `/{task_id}`
- **Method**: `DELETE`
- **URL Parameters**: 
  - `task_id` (UUID, required): ID of the task to delete
- **Authentication**: Required
- **Success Response**: 
  - Code: 204
  - Content: None
- **Error Response**: 
  - Code: 404
  - Content: `{"detail": "Resource Not Found"}`

## User API Documentation

This document outlines the API endpoints for managing user data.

### Base URL

All endpoints are prefixed with `/user`.

### Authentication

All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Endpoints

#### 1. Get All Users

Retrieves a list of users based on optional filter criteria.

- **URL**: `/`
- **Method**: `GET`
- **Query Parameters**:
  - `user_id` (UUID, optional): Filter by user ID
  - `username` (string, optional): Filter by username
  - `email` (string, optional): Filter by email
  - `is_active` (boolean, optional): Filter by active status
  - `is_admin` (boolean, optional): Filter by admin status
  - `page` (int, default=1): Page number for pagination
  - `size` (int, default=10, max=50): Number of items per page
- **Authentication**: Required
- **Success Response**: 
  - Code: 200 Ok
  - Content: 
  ```json
  {
    "id": "UUID",
    "email": "string",
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "company_id": "UUID",
    "is_active": "boolean",
    "is_admin": "boolean"
  }
  ```

#### 2. Get User by ID

Retrieves details of a specific user.

- **URL**: `/{user_id}`
- **Method**: `GET`
- **URL Parameters**: 
  - `user_id` (UUID, required): ID of the user to retrieve
- **Authentication**: Required
- **Success Response**: 
  - Code: 200 Ok
  - Content: 
  ```json
  {
    "id": "UUID",
    "email": "string",
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "company_id": "UUID",
    "is_active": "boolean",
    "is_admin": "boolean"
  }
  ```

- **Error Response**: 
  - Code: 404 Not Found
  - Content: `{"detail": "Resource Not Found"}`

#### 3. Create User

Creates a new user. Requires admin privileges.

- **URL**: `/`
- **Method**: `POST`
- **Request Body**: 
```json
{
  "company_id": "UUID",
  "email": "string",
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "password": "string",
  "is_active": "boolean",
  "is_admin": "boolean"
}
```
- **Authentication**: Required (Admin only)
- **Success Response**: 
  - Code: 200
  - Content: 
  ```json
  {
    "id": "UUID",
    "email": "string",
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "company_id": "UUID",
    "is_active": "boolean",
    "is_admin": "boolean"
  }
  ```

#### 4. Update User

Updates an existing user. Requires admin privileges.

- **URL**: `/{user_id}`
- **Method**: `PUT`
- **URL Parameters**: 
  - `user_id` (UUID, required): ID of the user to update
- **Request Body**: 
```json
{
  "email": "string",
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "password": "string",
  "is_active": "boolean",
  "is_admin": "boolean",
  "company_id": "UUID"
}
```
- **Authentication**: Required (Admin only)
- **Success Response**: 
  - Code: 201 Created
  - Content: 
  ```json
  {
    "id": "UUID",
    "email": "string",
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "company_id": "UUID",
    "is_active": "boolean",
    "is_admin": "boolean"
  }
  ```
- **Error Response**: 
  - Code: 404 Not Found
  - Content: `{"detail": "Resource Not Found"}`

#### 5. Delete User

Deletes a user. Requires admin privileges.

- **URL**: `/{user_id}`
- **Method**: `DELETE`
- **URL Parameters**: 
  - `user_id` (UUID, required): ID of the user to delete
- **Authentication**: Required (Admin only)
- **Success Response**: 
  - Code: 204 No Content
  - Content: None
- **Error Response**: 
  - Code: 404 Not Found
  - Content: `{"detail": "Resource Not Found"}`
