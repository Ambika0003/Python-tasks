import os
import pymysql
from config import Config

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), 'schema.sql')


def parse_sql_statements(sql_text):
    statements = []
    statement = ''
    for line in sql_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('--') or stripped.startswith('/*') or stripped.startswith('*/'):
            continue
        statement += line + '\n'
        if stripped.endswith(';'):
            statements.append(statement.strip())
            statement = ''
    if statement.strip():
        statements.append(statement.strip())
    return statements


def ensure_database_exists(connection):
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    connection.commit()


def reset_database():
    if not os.path.exists(SCHEMA_FILE):
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_FILE}")

    with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    statements = parse_sql_statements(schema_sql)
    connection_params = {
        'host': Config.DB_HOST,
        'port': int(Config.DB_PORT),
        'user': Config.DB_USER,
        'password': Config.DB_PASSWORD,
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
        'autocommit': False,
    }

    # Connect without specifying the database so we can create it if needed.
    conn = pymysql.connect(database=None, **connection_params)
    try:
        ensure_database_exists(conn)
    finally:
        conn.close()

    connection_params['database'] = Config.DB_NAME
    conn = pymysql.connect(**connection_params)
    try:
        with conn.cursor() as cursor:
            for stmt in statements:
                cursor.execute(stmt)
        conn.commit()
        print(f"Database '{Config.DB_NAME}' has been reset using '{SCHEMA_FILE}'.")
    finally:
        conn.close()


if __name__ == '__main__':
    reset_database()
