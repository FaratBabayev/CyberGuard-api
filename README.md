# CyberGuard API — Assignment 2 Prototype

## Project Overview

CyberGuard is a REST API prototype built with **FastAPI**. It simulates a cybersecurity incident management system using mocked in-memory data, token-based authentication, and role-based access control.

The prototype allows users to retrieve, create, update, and delete security incidents while enforcing access permissions.

**Important:** All incident data is stored in memory and resets whenever the server restarts. The prototype does not use a persistent database or a real authentication system.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/FaratBabayev/CyberGuard-api.git
cd CyberGuard-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, temporarily allow activation for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt (CMD):**

```cmd
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start the server

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

- **Greeting page:** http://127.0.0.1:8000/api/v1/greeting
- **Swagger API documentation:** http://127.0.0.1:8000/docs

## Authentication

The prototype uses predefined mock Bearer tokens. Include the appropriate token in the `Authorization` header:

```text
Authorization: Bearer YOUR_TOKEN
```

| User | Role | Token |
|---|---|---|
| User A | user | `user-a-token` |
| User B | user | `user-b-token` |
| Administrator | admin | `admin-token` |

Regular users can access and manage their own incidents, while the administrator can access and manage all incidents.

Missing or invalid tokens result in `401 Unauthorized`. Users attempting to access another user's incident receive `403 Forbidden`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/greeting` | Displays project and team information |
| GET | `/api/v1/incidents` | Retrieves incidents accessible to the authenticated user |
| GET | `/api/v1/incidents/{incident_id}` | Retrieves a specific incident |
| POST | `/api/v1/incidents` | Creates a new incident |
| PUT | `/api/v1/incidents/{incident_id}` | Updates an existing incident |
| DELETE | `/api/v1/incidents/{incident_id}` | Deletes an incident |

The greeting endpoint is publicly accessible. Incident endpoints require a valid Bearer token.

The incident listing endpoint supports the following query parameters:

- `page`: Page number.
- `perPage`: Number of incidents per page.
- `status`: Filter incidents by status.
- `severity`: Filter incidents by severity.

## Example Requests

The following examples use `curl` to demonstrate the main API operations.

### 1. List incidents

```bash
curl -H "Authorization: Bearer user-a-token" \
http://127.0.0.1:8000/api/v1/incidents
```

### 2. Retrieve a specific incident

```bash
curl -H "Authorization: Bearer user-a-token" \
http://127.0.0.1:8000/api/v1/incidents/inc_101
```

### 3. Create an incident

```bash
curl -X POST http://127.0.0.1:8000/api/v1/incidents \
-H "Authorization: Bearer user-a-token" \
-H "Content-Type: application/json" \
-d '{
  "title": "Suspicious sudo usage",
  "severity": "Medium",
  "description": "Unusual sudo activity detected.",
  "status": "Open",
  "sourceIp": "10.0.0.5"
}'
```

### 4. Update an incident

```bash
curl -X PUT http://127.0.0.1:8000/api/v1/incidents/inc_101 \
-H "Authorization: Bearer user-a-token" \
-H "Content-Type: application/json" \
-d '{
  "title": "Updated suspicious sudo usage",
  "severity": "High",
  "description": "Further investigation required.",
  "status": "Investigating",
  "sourceIp": "10.0.0.5"
}'
```

### 5. Delete an incident

```bash
curl -X DELETE http://127.0.0.1:8000/api/v1/incidents/inc_101 \
-H "Authorization: Bearer user-a-token"
```

**Note:** These examples modify the in-memory incident data. Restarting the server restores the predefined mock data.

## Authorization and Error Handling

The API includes centralized error handling and structured error responses.

| Status Code | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Resource created |
| 400 | Invalid request data |
| 401 | Missing or invalid authentication token |
| 403 | Authenticated user does not have permission |
| 404 | Incident does not exist |
| 409 | Duplicate incident |
| 500 | Unexpected server error |

A regular user accessing another user's incident receives `403 Forbidden`, making the authorization failure explicit.

The `HIDE_FOREIGN_INCIDENTS` setting in `app/routes/incidents.py` can be switched to `True` to return `404 Not Found` instead.

## Mock Incident Data

The prototype starts with five predefined incidents:

- Two incidents belonging to User A.
- Two incidents belonging to User B.
- One incident belonging to the Administrator.

Incident data is stored in an in-memory data structure. New incidents receive generated IDs, and all changes are temporary.

## Running Tests

Install the development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the automated test suite:

```bash
python -m pytest
```

## API Documentation

Interactive API documentation is provided through Swagger UI:

http://127.0.0.1:8000/docs

Swagger allows users to inspect available endpoints, provide authentication tokens, send requests, and examine API responses.

## Project Structure

```text
CyberGuard-api/
│
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── errors.py
│   ├── mock_data.py
│   ├── responses.py
│   ├── validation.py
│   │
│   └── routes/
│       ├── greeting.py
│       └── incidents.py
│
├── tests/
│   └── test_api.py
│
├── .gitignore
├── README.md
├── CONTRIBUTORS.md
├── requirements.txt
└── requirements-dev.txt
```

## Contributors and Responsibilities

The project was developed collaboratively using Git feature branches and GitHub pull requests.

| Team Member | Responsibilities |
|---|---|
| **Farat Babayev (22781)** | Implemented the main application setup (`main.py`), centralized error handling (`errors.py`), response formatting (`responses.py`), and automated tests. Coordinated project integration, reviewed pull requests, and handled merges into the main branch. |
| **Farid Guliyev (21464)** | Implemented the HTML greeting endpoint (`greeting.py`) and incident API routes (`incidents.py`), including incident retrieval and CRUD operations. Responsible for the README documentation and `requirements.txt`. |
| **Elgun Atayev (20561)** | Implemented authentication and role-based access control (`auth.py`), predefined mock incident data (`mock_data.py`), and request validation (`validation.py`). Responsible for `CONTRIBUTORS.md`, `.gitignore`, and `requirements-dev.txt`. |

## Git Commit History

The following output shows the number of commits attributed to each contributor:

```text
  9 FaratBabayev
  3 Farid-Guliyev
  3 elgunns
```

To view the commit summary, run:

```bash
git fetch --all
git shortlog -sn --all
```

Commit counts represent recorded Git commits and do not necessarily reflect the total amount of work completed by each contributor. Pull requests themselves are not commits, although the commits included in them are counted.