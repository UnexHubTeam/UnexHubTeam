# Agent databases: PostgreSQL and MySQL

[Documentation home](README.md) · [Mode A guide](agent-development-mode-a.md) · [Mode B guide](agent-development-upload.md) · [简体中文](../zh-CN/agent-databases.md)

Updated: 2026-10-21

Container Agents in Mode A or Mode B can provision an optional PostgreSQL database, MySQL database, or both for each user of an Agent. UnexHub prepares the databases at instance startup and injects connection settings into the container environment. Your **backend** reads those settings; database setup is managed through UnexHub.

The UnexHub deployment form's live catalog determines available engines, versions, and connection limits. Managed SQL stores application records independently of container files. It does not provide file persistence or change the model-access requirements of the selected deployment mode.

## On this page

- [Configure database requirements](#database-configuration)
- [Injected environment variables](#database-environment)
- [Provisioning, reuse, and version changes](#database-lifecycle)
- [PostgreSQL backend example](#postgresql-example)
- [MySQL backend example](#mysql-example)
- [Connection pools, credentials, and release checks](#database-practices)

<a id="database-configuration"></a>
## Configure database requirements

1. Open **Agent deployment configuration** and select **Mode A · Unexhub Containers** or **Mode B · Cloudflare Containers**.
2. In **Minimum resource requirements**, find **Database configuration** below the compute specification settings. It is empty by default; Agents that do not need SQL can leave it empty.
3. Select **Add database**, then select the engine and version from the two dropdowns. PostgreSQL and MySQL are supported, with at most one entry per engine. Add another row to use both. Redis and MongoDB are disabled because they are not implemented yet.
4. Read the displayed limits and TLS mode, then save the runtime configuration. Database requirements are included in the version submitted for review. Changing them after publication takes the Agent off the market and requires another review; ordinary-user startup uses the approved version's snapshot, while developer self-tests use the working configuration.
5. Test using a **new instance**. Existing running instances keep their original environment; stop and start again after changing the requirements.

The catalog shows the default maximum connections for a database login and its SSL/TLS mode. The injected `CONNECTION_LIMIT` describes the actual allocated database login; it can differ from a later catalog default.

If the catalog is unavailable, an engine is not ready, or no version is selectable, contact UnexHub support with the Agent ID and sanitized error. Database connection settings are supplied by UnexHub at startup; do not add passwords through custom environment variables.

<a id="database-environment"></a>
## Injected environment variables

Only selected engines receive variables. A PostgreSQL-only Agent receives no `UNEX_DATABASE_MYSQL_*` variables. All values are environment strings. For `single` and `frontend-package` topologies, the backend container receives them; for `split`, only the backend receives them. They are never injected into the frontend container or a frontend build.

| PostgreSQL variable | MySQL variable | Meaning |
| --- | --- | --- |
| `UNEX_DATABASE_POSTGRESQL_HOST` | `UNEX_DATABASE_MYSQL_HOST` | Connection host; may be a configured pool endpoint |
| `UNEX_DATABASE_POSTGRESQL_PORT` | `UNEX_DATABASE_MYSQL_PORT` | Connection port; parse as an integer when required by the driver |
| `UNEX_DATABASE_POSTGRESQL_DATABASE` | `UNEX_DATABASE_MYSQL_DATABASE` | Allocated physical database name; do not derive it from a user ID |
| `UNEX_DATABASE_POSTGRESQL_USERNAME` | `UNEX_DATABASE_MYSQL_USERNAME` | Login scoped to this database |
| `UNEX_DATABASE_POSTGRESQL_PASSWORD` | `UNEX_DATABASE_MYSQL_PASSWORD` | Password for that database login |
| `UNEX_DATABASE_POSTGRESQL_URL` | `UNEX_DATABASE_MYSQL_URL` | Full connection URI, including encoded credentials and SSL settings |
| `UNEX_DATABASE_POSTGRESQL_SSL_MODE` | `UNEX_DATABASE_MYSQL_SSL_MODE` | Configured TLS mode: `disable`, `prefer`, `require`, `verify-ca`, or `verify-full` |
| `UNEX_DATABASE_POSTGRESQL_CONNECTION_MODE` | `UNEX_DATABASE_MYSQL_CONNECTION_MODE` | `direct` or `pooled` |
| `UNEX_DATABASE_POSTGRESQL_CONNECTION_LIMIT` | `UNEX_DATABASE_MYSQL_CONNECTION_LIMIT` | Actual maximum connections for the allocated database login |

The backend must explicitly read these variables; injection does not configure an ORM automatically. Use the provided host, port, database, and login without assuming a default port or physical name. Preserve the configured TLS behavior. Some MySQL clients do not understand the platform URI's SSL parameters; the example below uses individual fields and an explicit TLS context.

Injected connection variables do not grant network access. In Mode A, native database connections require an administrator to allow the actual database TCP address and port through global rules, with appropriate hostname-resolution permissions. An HTTP/HTTPS domain permission does not replace database TCP access. For timeouts, give platform support the Agent ID and a sanitized error.

`UNEX_` is reserved. Do not manually add these names through **Add environment variable**. Custom environment variables are stored as plaintext and must contain only non-sensitive application settings. Database connection settings are injected at container creation, outside the editable runtime configuration and instance/billing snapshots.

<a id="database-lifecycle"></a>
## Provisioning, reuse, and version changes

- On first use, UnexHub prepares a separate database and database-scoped login for each selected engine, associated with the current user and Agent.
- Preparation happens before compute pre-deduction and container creation. A preparation failure prevents those steps; if one engine was already provisioned before another failed, it is retained for a retry.
- Repeated or concurrent starts and image updates reuse the database for the same **user × Agent × engine**. Another user or Agent receives a separate database and login. New sessions do not create a fresh empty database.
- Each database has an independent SQL login. An Agent does not automatically receive access to another Agent's databases or another user's data. Future Agent collaboration needs explicit platform authorization.
- Selecting another version does not upgrade, migrate, or recreate an existing database. A mismatch between the selected version and the allocated server version blocks startup. Coordinate migration with the platform operator and keep application schemas compatible with release and rollback requirements.
- Stopping a container, removing a database requirement, or deleting an Agent does not automatically delete its remote database. Do not present any of those actions as data erasure; retention and database cleanup require separate management.

SQL data persists independently of container disk. Container files remain temporary, and managed SQL does not provide a D1/R2 file workspace or an upload/download broker.

## Run the backend examples

Use Python 3.10+ in the Agent backend. Add these dependencies to your project, then lock the resolved versions for releases:

```bash
python -m pip install 'psycopg[binary]>=3.2,<4' 'PyMySQL[rsa]>=1.1,<1.2'
```

Run the examples inside a platform-launched test container after selecting the corresponding database. They create `agent_example_notes` and insert or update row `id=1`; use a disposable test Agent/database. They open one connection, run parameterized SQL, commit a write, read it back, and close the connection. Connection credentials come from UnexHub's injected environment variables.

<a id="postgresql-example"></a>
## PostgreSQL backend example

[Download `postgresql_example.py`](../../examples/agent-databases/postgresql_example.py), then run `python postgresql_example.py` in the test container. The injected URI preserves credential escaping and `sslmode`. Psycopg's connection context commits on success, rolls back on error, and closes the connection. See the [Psycopg usage guide](https://www.psycopg.org/psycopg3/docs/basic/usage.html).

```python
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
```

For certificate verification with a private CA, include the public CA certificate in the image and set a non-sensitive application setting such as `DATABASE_CA_FILE=/app/certs/database-ca.pem`. This optional setting is **not** injected by the platform. `verify-full` checks the certificate chain and hostname; `require` alone does not guarantee server identity verification. See [PostgreSQL SSL modes](https://www.postgresql.org/docs/current/libpq-ssl.html).

<a id="mysql-example"></a>
## MySQL backend example

[Download `mysql_example.py`](../../examples/agent-databases/mysql_example.py), then run `python mysql_example.py` in the test container. This example translates the injected SSL mode into an `ssl.SSLContext`; it does not assume a driver can consume the URL unchanged. See [PyMySQL connection options](https://pymysql.readthedocs.io/en/latest/modules/connections.html).

```python
"""Backend-only MySQL example. Run in a disposable Agent test database."""

import os
import ssl

import pymysql


def required(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing {name}; enable the database and restart the instance")
    return value


def mysql_tls(mode):
    if mode == "disable":
        return None
    if mode not in {"prefer", "require", "verify-ca", "verify-full"}:
        raise RuntimeError("Unsupported database TLS mode")
    context = ssl.create_default_context(cafile=os.environ.get("DATABASE_CA_FILE"))
    if mode in {"prefer", "require"}:
        # These configured modes do not verify server certificates.
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    elif mode == "verify-ca":
        context.check_hostname = False
    return context


def main():
    prefix = "UNEX_DATABASE_MYSQL_"
    mode = required(prefix + "SSL_MODE")
    with pymysql.connect(
        host=required(prefix + "HOST"),
        port=int(required(prefix + "PORT")),
        user=required(prefix + "USERNAME"),
        password=required(prefix + "PASSWORD"),
        database=required(prefix + "DATABASE"),
        charset="utf8mb4",
        connect_timeout=5,
        read_timeout=15,
        write_timeout=15,
        autocommit=False,
        local_infile=False,
        ssl=mysql_tls(mode),
        ssl_disabled=(mode == "disable"),
    ) as conn:
        # PyMySQL 1.1 can fall back when a server does not advertise TLS.
        # Fail closed when the configured mode requires TLS.
        if mode not in {"disable", "prefer"} and not getattr(conn, "_secure", False):
            raise RuntimeError("The database connection requires TLS")
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS agent_example_notes "
                    "(id integer PRIMARY KEY, body text NOT NULL)"
                )
                cursor.execute(
                    "INSERT INTO agent_example_notes (id, body) VALUES (%s, %s) "
                    "ON DUPLICATE KEY UPDATE body = %s",
                    (1, "Hello from this user's Agent", "Hello from this user's Agent"),
                )
                cursor.execute("SELECT body FROM agent_example_notes WHERE id = %s", (1,))
                if cursor.fetchone() != ("Hello from this user's Agent",):
                    raise RuntimeError("Database read-back failed")
            conn.commit()
        except Exception:
            conn.rollback()
            raise
    # MySQL DDL may commit independently; migrations need their own recovery strategy.
    print("MySQL write/read succeeded.")


if __name__ == "__main__":
    try:
        main()
    except (pymysql.Error, OSError, ValueError, RuntimeError):
        raise SystemExit(
            "MySQL operation failed; check database configuration, TLS and connectivity."
        ) from None
```

The example honors the configured mode: `disable` turns TLS off; `prefer` attempts TLS where supported; `require` demands encryption; `verify-ca` also checks the certificate chain; `verify-full` also checks the hostname. `prefer` and `require` do not verify certificates in this MySQL example. Use `DATABASE_CA_FILE` for a private CA when verification is enabled; ask the platform operator to correct certificate problems rather than weakening the configured mode. The `_secure` check uses a PyMySQL 1.1 attribute to prevent required TLS from silently falling back; revalidate it if you replace or upgrade the driver. MySQL DDL can commit independently, so schema migrations need their own recovery plan.

<a id="database-practices"></a>
## Connection pools, credentials, and release checks

For a production backend, bound the pool using the selected engine's `CONNECTION_LIMIT`. Count connections from **all processes and containers** using this user–Agent database login, including workers and migrations; leave headroom instead of assigning the full limit to every process. Close connections on shutdown, set timeouts, and handle unavailable capacity without unlimited retries. Check `CONNECTION_MODE` before choosing session-dependent SQL features with a pool endpoint.

The injected database password and URL are readable by your container and its dependencies. Keep them in the backend process, avoid logging raw driver errors, and never return them through a configuration endpoint, frontend bundle, browser storage, support report, or page URL.

Before release, verify writes and reads, persistence after stopping and starting, reuse after an image update, and isolation between two users and between two Agents. Test missing variables, TLS and connection-limit failures with sanitized user-facing errors. Also complete the release checks for your selected deployment mode: [Mode A](agent-development-mode-a.md#section-10) or [Mode B](agent-development-upload.md#section-10).
