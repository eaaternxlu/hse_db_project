import psycopg2
from app.config import DB_CONFIG


def execute_procedure(procedure, *params):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        if procedure.startswith("display_") or procedure.startswith("search_"):
            cur.callproc(procedure, params)
            result = cur.fetchall() if cur.description else None
        else:
            placeholders = ", ".join(["%s"] * len(params))
            query = f"CALL {procedure}({placeholders});"
            cur.execute(query, params)
            conn.commit()
            result = None

        cur.close()
        conn.close()
        return result
    except Exception as e:
        raise RuntimeError(f"Database error: {e}")
