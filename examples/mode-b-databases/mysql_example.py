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
