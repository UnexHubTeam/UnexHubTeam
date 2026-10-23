"""Backend-only PostgreSQL example. Run in a disposable Agent test database."""

import os

import psycopg


def required(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing {name}; enable the database and restart the instance")
    return value


def main():
    options = {"connect_timeout": 5}
    if os.environ.get("DATABASE_CA_FILE"):
        options["sslrootcert"] = os.environ["DATABASE_CA_FILE"]

    # The injected URL already includes encoded credentials and sslmode.
    with psycopg.connect(required("UNEX_DATABASE_POSTGRESQL_URL"), **options) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS agent_example_notes "
                "(id integer PRIMARY KEY, body text NOT NULL)"
            )
            cursor.execute(
                "INSERT INTO agent_example_notes (id, body) VALUES (%s, %s) "
                "ON CONFLICT (id) DO UPDATE SET body = EXCLUDED.body",
                (1, "Hello from this user's Agent"),
            )
            cursor.execute("SELECT body FROM agent_example_notes WHERE id = %s", (1,))
            if cursor.fetchone() != ("Hello from this user's Agent",):
                raise RuntimeError("Database read-back failed")
    # The context commits on success, rolls back on error, and closes the connection.
    print("PostgreSQL write/read succeeded.")


if __name__ == "__main__":
    try:
        main()
    except (psycopg.Error, OSError, ValueError, RuntimeError):
        # Raw driver exceptions can contain connection details. Sanitize user-facing errors.
        raise SystemExit(
            "PostgreSQL operation failed; check database configuration, TLS and connectivity."
        ) from None
