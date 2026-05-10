import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "db" / "ctfpilot.db"

def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            target TEXT NOT NULL,
            platform TEXT NOT NULL,
            started_at TEXT NOT NULL,
            finished_at TEXT,
            status TEXT DEFAULT 'active'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            flag_type TEXT NOT NULL,
            value TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        )
    """)
    conn.commit()
    conn.close()

def create_session(name: str, target: str, platform: str) -> int:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (name, target, platform, started_at) VALUES (?, ?, ?, ?)",
        (name, target, platform, datetime.now().isoformat())
    )
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

def get_active_session():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM sessions WHERE status = 'active' ORDER BY started_at DESC LIMIT 1"
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "target": row[2], 
                "platform": row[3], "started_at": row[4]}
    return None

def add_note(session_id: int, content: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (session_id, content, created_at) VALUES (?, ?, ?)",
        (session_id, content, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def add_flag(session_id: int, flag_type: str, value: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO flags (session_id, flag_type, value, created_at) VALUES (?, ?, ?, ?)",
        (session_id, flag_type, value, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_session_data(session_id: int) -> dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
    session = cursor.fetchone()
    cursor.execute("SELECT content, created_at FROM notes WHERE session_id = ?", (session_id,))
    notes = cursor.fetchall()
    cursor.execute("SELECT flag_type, value, created_at FROM flags WHERE session_id = ?", (session_id,))
    flags = cursor.fetchall()
    conn.close()
    return {
        "session": session,
        "notes": notes,
        "flags": flags
    }