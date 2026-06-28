import sqlite3
from datetime import datetime

DB_PATH = "database/metadata.db"


# -------------------------
# Initialize database
# -------------------------
def init_db():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # -------------------------
    # Documents Table
    # -------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        upload_time TEXT,
        chunk_count INTEGER
    )
    """)

    # -------------------------
    # Query Logs Table
    # -------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        timestamp TEXT,
        retrieved_chunks INTEGER
    )
    """)

    # -------------------------
    # Users Table
    # -------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # -------------------------
    # Insights Table
    # -------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        insight TEXT,
        timestamp TEXT
    )
    """)

    # -------------------------
    # Chat History Table
    # -------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_question TEXT,
        ai_answer TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


# -------------------------
# Save uploaded file info
# -------------------------
def save_document(filename, chunk_count):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO documents (filename, upload_time, chunk_count)
        VALUES (?, ?, ?)
    """, (
        filename,
        datetime.now().isoformat(),
        chunk_count
    ))

    conn.commit()
    conn.close()


# -------------------------
# Save query logs
# -------------------------
def save_query(question, retrieved_chunks):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO queries (question, timestamp, retrieved_chunks)
        VALUES (?, ?, ?)
    """, (
        question,
        datetime.now().isoformat(),
        len(retrieved_chunks)
    ))

    conn.commit()
    conn.close()


# -------------------------
# Save Chat History
# -------------------------
def save_chat(user_question, ai_answer):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_history (
            user_question,
            ai_answer,
            timestamp
        )
        VALUES (?, ?, ?)
    """, (
        user_question,
        ai_answer,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


# -------------------------
# Get Chat History
# -------------------------
def get_chat_history():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_question, ai_answer
        FROM chat_history
        ORDER BY id ASC
    """)

    chats = cursor.fetchall()

    conn.close()

    return chats