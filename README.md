# Automated Containerized Data Pipeline (API → SQL Warehouse)

## Overview
This project is a fully functional, production-ready **Extract, Transform, Load (ETL)** data infrastructure system. Rather than relying on loose, standalone Python scripts that process local files, it builds a complete data lifecycle — programmatically connecting to a live web API, capturing raw user profile data, cleaning and standardizing fields with Python, and loading the results into a local SQL data warehouse built on SQLite. The entire application is packaged inside a Docker container, so it runs consistently across any environment (local machines, AWS, or production servers) without manual dependency installation or database configuration.

---

## Pipeline Architecture

The system is broken into three isolated, modular phases orchestrated by a central entry point (`main.py`):

### 1. Extraction — `pipelines/extract.py`
Establishes an HTTP connection to the [RandomUser.me](https://randomuser.me) API, which serves as a live data source. It pulls 10 raw user profiles per request. The raw response is nested and unstructured. The script automatically creates a `data/` landing zone directory if one doesn't exist, then writes the payload to `raw_users.json`.

### 2. Transformation — `pipelines/transform.py`
Reads the raw JSON file from the landing zone and flattens the nested structure (e.g., name fields buried inside a `name` object) so the data fits cleanly into a relational table. It also strips unnecessary fields (such as image URLs and phone numbers) and standardizes formatting — emails are lowercased and names are properly capitalized.

### 3. Loading — `pipelines/load.py`
Connects to a local SQLite database file (`data/pipeline_database.db`), which lives directly in the project directory for easy deployment and version tracking. It creates a structured `users` table with the columns `id`, `first_name`, `last_name`, `email`, `country`, and `age`. The loader uses **UPSERT** logic (`ON CONFLICT DO UPDATE`), an industry-standard pattern that updates existing records on repeat pipeline runs instead of crashing or producing duplicate rows.

---

## Tech Stack

| Tool | Role |
|---|---|
| **Python** | Core language for extraction and transformation logic |
| **Docker** | Containerizes the app and manages all dependencies |
| **SQLite** | Lightweight relational database engine for the local warehouse |
| **Requests** | Handles HTTP connections and API calls |

---

## How to Run

Since the project is fully containerized, you do not need Python or any packages installed on your host machine — Docker handles everything.

### 1. Build the Image
From the root of the project directory, run:
```bash
docker build -t automated-etl-pipeline .
```

### 2. Run the Container
Use a volume mount to ensure the database file is saved to your local workspace:
```bash
docker run --rm -v $(pwd)/data:/app/data automated-etl-pipeline
```

### 3. Inspect the Data Warehouse
Once the container finishes, query the database directly from your terminal using the SQLite CLI:
```bash
sqlite3 data/pipeline_database.db
```

Your prompt will change to `sqlite>`. Run standard SQL to inspect the loaded records:
```sql
-- Count successfully ingested rows
SELECT COUNT(*) FROM users;

-- Preview cleaned user profiles
SELECT first_name, last_name, email, country, age FROM users LIMIT 3;
```

Type `.exit` to return to your normal terminal prompt.