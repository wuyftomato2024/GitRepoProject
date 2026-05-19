# GitRepoProject

## Overview

GitRepoProject is a FastAPI backend project for syncing GitHub repository data into a local MySQL database.

The current workflow is:

1. Accept a GitHub username
2. Load repository data
3. Compare the incoming data with local database records
4. Insert new repositories
5. Update changed repository fields
6. Mark missing repositories as deleted

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- MySQL
- PyMySQL
- Pydantic
- Requests
- Uvicorn

## File Structure

```text
GitRepoProject/
|-- .gitignore
|-- README.md
|-- READMECN.md
|-- requirements.txt
`-- app/
    |-- main.py
    |-- core/
    |   `-- db_table.py
    |-- mock_data/
    |   `-- gitRepo_mock_data.py
    |-- repositories/
    |   `-- repositories.py
    |-- schema/
    |   |-- database.py
    |   `-- model.py
    `-- service/
        |-- dataSync_service.py
        `-- github_service.py
```

## Main Files

- `app/main.py`
  FastAPI entrypoint. Creates tables, manages DB sessions, and exposes the sync API.

- `app/service/dataSync_service.py`
  Core sync logic for comparing incoming repo data with local DB data.

- `app/service/github_service.py`
  GitHub API fetch helper for loading repository data.

- `app/repositories/repositories.py`
  Data access layer for reading and updating `github_repos` records.

- `app/core/db_table.py`
  SQLAlchemy table model definition.

- `app/schema/database.py`
  Database engine and session configuration.

- `app/mock_data/gitRepo_mock_data.py`
  Mock repository data used during local sync verification.

## API

### Sync Endpoint

```text
GET /repo_name?github_user=<username>
```

Behavior:

- Query existing records for the given GitHub user
- Load repository data
- Compare repositories by `repo_full_name`
- Create new rows for new repositories
- Update changed metadata such as stars, forks, description, and language
- Mark missing repositories with `is_deleted = True`

## Database Table

### `github_repos`

Main fields:

- `id`
- `github_user`
- `repo_name`
- `repo_full_name`
- `description`
- `language`
- `forks`
- `repo_url`
- `stars`
- `is_deleted`
- `updated_at`

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare MySQL

The current project uses the database connection defined in:

- `app/schema/database.py`

Current connection string:

```text
mysql+pymysql://root:tomato123@localhost/test_db
```

### 3. Start the server

```bash
uvicorn app.main:app --reload
```

### 4. Open the API

```text
http://127.0.0.1:8000/docs
```

## Notes

- The project is focused on local sync logic and repository comparison.
- Repository deletion is handled as a soft delete through the `is_deleted` field.
