# Streamlit Arango Demo

An interactive demo application that shows how to use [ArangoDB](https://www.arangodb.com/) with [Streamlit](https://streamlit.io/). Run AQL queries directly from a web UI, inspect execution plans, view results, and manage query tracking — all without writing any backend code.

---

## Features

- **AQL query editor** – write and execute [ArangoDB Query Language (AQL)](https://docs.arangodb.com/stable/aql/) queries from the browser.
- **Query preview** – syntax-highlighted preview of the current query before execution.
- **Bind variables** – supply named bind parameters via an editable table.
- **Execution plan & validation** – inspect the query plan and validate the query before running it.
- **Results table** – paginated display of query results.
- **Sidebar utilities**
  - View currently running queries.
  - View and clear slow queries.
  - Read and update query tracking properties.
  - Kill a running query by ID.

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.11+ |
| [Pipenv](https://pipenv.pypa.io/) | any recent |
| [Docker](https://www.docker.com/) | any recent (for local ArangoDB) |

---

## Installation

```bash
# Clone the repository
git clone https://github.com/Skitionek/streamlit-arango-demo.git
cd streamlit-arango-demo

# Install Python dependencies
pipenv install
```

---

## Configuration

The app reads ArangoDB connection details from environment variables **or** from a Streamlit secrets file (`.streamlit/secrets.toml`).

### Option A – Streamlit secrets file (recommended for local dev)

Copy the provided template and fill in your values:

```bash
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
```

```toml
# .streamlit/secrets.toml
ARANGO_HOST     = "http://localhost:8529"
ARANGO_DATABASE = "test"
ARANGO_USERNAME = "root"
ARANGO_PASSWORD = "yourpassword"
```

### Option B – Environment variables

```bash
export ARANGO_HOST="http://localhost:8529"
export ARANGO_DATABASE="test"
export ARANGO_USERNAME="root"
export ARANGO_PASSWORD="yourpassword"
```

| Variable | Default | Description |
|---|---|---|
| `ARANGO_HOST` | `http://localhost:8529` | ArangoDB server URL |
| `ARANGO_DATABASE` | `test` | Database name |
| `ARANGO_USERNAME` | *(required)* | Database username |
| `ARANGO_PASSWORD` | *(required)* | Database password |

---

## Running a Local ArangoDB Instance

The `Pipfile` includes a convenience script that starts ArangoDB in Docker:

```bash
pipenv run local_arango
```

This runs:

```
docker run --rm \
  -e ARANGO_RANDOM_ROOT_PASSWORD=1 \
  -v $PWD/arangodb_data:/var/lib/arangodb3 \
  -p 8529:8529 \
  --name arangodb-instance \
  arangodb
```

The generated root password is printed to the console on first start. Copy it into your `secrets.toml` or environment variable.

---

## Running the App

```bash
pipenv run streamlit run app.py
```

Open your browser at <http://localhost:8501>.

---

## Running the Tests

```bash
pipenv run pytest
```

The test suite uses Streamlit's built-in `AppTest` helper to verify the app starts without errors.

---

## Project Structure

```
streamlit-arango-demo/
├── app.py                          # Main Streamlit application
├── streamlit_arango_demo/
│   └── config.py                   # Configuration (env vars + Streamlit secrets)
├── tests/
│   └── test_app.py                 # App smoke tests
├── .streamlit/
│   ├── config.toml                 # Streamlit server configuration
│   └── secrets.toml.template       # Template for local secrets
├── arangodb_data/                  # Persistent ArangoDB data (Docker volume)
├── Pipfile                         # Python dependencies & scripts
└── Pipfile.lock
```

---

## License

This project is provided as a demo. See the repository for license details.
