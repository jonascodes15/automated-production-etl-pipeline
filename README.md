# Automated Containerized Data Pipeline (API to SQL Warehouse)

## What This Project Is All About
This project is a fully functional, production-ready **Extract, Transform, Load (ETL)** data infrastructure system. Instead of just running random, loose Python scripts that process local files, this system builds a complete data lifecycle. 

It programmatically hooks into a live web API data engine, captures raw user profile streams, cleans and standardizes the messy fields using Python, and builds a local SQL data warehouse using SQLite. The entire application is packaged inside a Docker container so it can run smoothly on any machine (AWS, a local PC, or production servers) without needing to manually install dependencies or configure database drivers.

---

## The Core Data Pipeline Flow

The system breaks down the heavy engineering lifting into three isolated, highly modular phases managed by a central orchestrator (`main.py`):

1. Extraction Phase (`pipelines/extract.py`)
   * How it works: It establishes an HTTP connection to a third-party API endpoint (`randomuser.me`) which acts as a data generator vending machine. 
   * The Data: It pulls 10 raw user profiles simultaneously. This response data is nested and messy.
   * The Output: The script automatically creates a `data/` landing zone folder if it doesn't exist and captures the payload into a physical file named `raw_users.json`.

2. Transformation Phase (`pipelines/transform.py`)
   * How it works: It reads the raw JSON file from the landing zone. Because API data often comes with nested dictionaries (like names tucked deep inside a `name` object), this script flattens the structure so it can easily fit into a relational database table.
   * Data Cleanliness: It strips away unneeded parameters (like image URLs or phone numbers) and standardizes formatting—forcing all user emails to lowercase and capitalizing names cleanly.

3. Loading Phase (`pipelines/load.py`)
   * How it works: It connects to a local database engine file (`data/pipeline_database.db`). Choosing SQLite means the data warehouse lives right inside our project directory, making it perfect for rapid deployment and easy tracking on GitHub.
   * The Schema & Guardrails: It sets up a rigid SQL table structure with custom columns (`id`, `first_name`, `last_name`, `email`, `country`, `age`). It uses **UPSERT** logic (`ON CONFLICT DO UPDATE`), which is a major data engineering standard—if you run this pipeline multiple times and get a user that already exists, it updates their current record instead of crashing or creating duplicate data rows.

---

## Tech Stack Used
* Python : The core language powering our extraction logic and data transformation.
* Docker: Containerizes the app, baking Python and our library requirements into an isolated environment.
* SQLite: A lightweight, robust relational database engine that handles standard SQL queries.
* Requests Library: Handles the network calls and API connections smoothly.

---

## Step-by-Step: How to Run the Pipeline

Since the project is containerized, you don't need to install Python or Pip packages on your host machine. Docker will handle everything.

### 1. Build the System Image
Open your terminal at the root of the project folder and run:
```bash
docker build -t automated-etl-pipeline .
```

### 2. Execute the Automated Container
To run the pipeline container and ensure the database file saves straight to your workspace folder, use this volume mount run command:
```bash
docker run --rm -v $(pwd)/data:/app/data automated-etl-pipeline
```

### 3. Inspecting the SQL Warehouse Data
Once the container finishes executing, your data is officially locked into the SQL database. You can drop straight into the database file using the SQLite command-line tool right in your terminal:

```bash
sqlite3 data/pipeline_database.db
```

Your terminal prompt will change to `sqlite>`. Now you can run standard SQL queries to inspect the cleaned records:

```sql
-- See the total count of successfully ingested rows
SELECT COUNT(*) FROM users;

-- Look at a slice of the actual cleaned profiles
SELECT first_name, last_name, email, country, age FROM users LIMIT 3;
```

To exit the database console and return to your normal terminal prompt, simply type: `.exit`