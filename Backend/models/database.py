import sqlite3
from datetime import datetime

DB_PATH = "database/metadata.db"


# =========================
# INIT DATABASE
# =========================
def init_db():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # =========================
    # DOCUMENTS TABLE
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            upload_time TEXT,
            chunk_count INTEGER
        )
    """)

    # =========================
    # QUERY LOGS TABLE
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            timestamp TEXT,
            retrieved_chunks INTEGER
        )
    """)

    # =========================
    # USERS TABLE
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # =========================
    # INSIGHTS TABLE (future AI summaries)
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            insight TEXT,
            timestamp TEXT
        )
    """)

    # =========================
    # CHAT HISTORY TABLE
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_question TEXT,
            ai_answer TEXT,
            timestamp TEXT
        )
    """)

    # =========================
    # MEMORY TIMELINE TABLE
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory_timeline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_text TEXT,
            event_type TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================
# SAVE DOCUMENT
# =========================
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


# =========================
# SAVE QUERY
# =========================
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


# =========================
# SAVE CHAT (IMPORTANT FOR INSIGHTS)
# =========================
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


# =========================
# GET CHAT HISTORY
# =========================
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