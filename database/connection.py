# database/connection.py

import sqlite3
import os
from datetime import datetime

DB_PATH = "github_analyzer.db"


# ════════════════════════════════
# INITIALIZE DATABASE
# ════════════════════════════════
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            avatar_url TEXT,
            auth_provider TEXT DEFAULT 'google',
            github_username TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Search history table
    c.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            github_username TEXT NOT NULL,
            mode TEXT DEFAULT 'quick',
            job_role TEXT,
            experience_level TEXT,
            total_score REAL,
            career_score REAL,
            ats_score REAL,
            searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Leaderboard table
    c.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            github_username TEXT UNIQUE NOT NULL,
            name TEXT,
            avatar_url TEXT,
            developer_type TEXT,
            total_score REAL,
            job_role TEXT,
            experience_level TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Notifications table
    c.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            message TEXT,
            sent_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()
    print("[OK] Database initialized successfully!")


# ════════════════════════════════
# USER FUNCTIONS
# ════════════════════════════════
def create_or_update_user(email, name, avatar_url, auth_provider, github_username=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO users (email, name, avatar_url, auth_provider, github_username)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(email) DO UPDATE SET
            name=excluded.name,
            avatar_url=excluded.avatar_url,
            github_username=COALESCE(excluded.github_username, github_username),
            last_login=CURRENT_TIMESTAMP
    """, (email, name, avatar_url, auth_provider, github_username))
    conn.commit()

    c.execute("SELECT id FROM users WHERE email=?", (email,))
    user_id = c.fetchone()[0]
    conn.close()
    return user_id


def get_user_by_email(email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "email": row[1],
            "name": row[2],
            "avatar_url": row[3],
            "auth_provider": row[4],
            "github_username": row[5],
            "created_at": row[6],
            "last_login": row[7],
        }
    return None


def update_github_username(user_id, github_username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        UPDATE users SET github_username=? WHERE id=?
    """, (github_username, user_id))
    conn.commit()
    conn.close()


# ════════════════════════════════
# SEARCH HISTORY FUNCTIONS
# ════════════════════════════════
def save_search(
    github_username,
    mode="quick",
    job_role=None,
    experience_level=None,
    total_score=None,
    career_score=None,
    ats_score=None,
    user_id=None
):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO search_history
        (user_id, github_username, mode, job_role,
         experience_level, total_score, career_score, ats_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, github_username, mode, job_role,
          experience_level, total_score, career_score, ats_score))
    conn.commit()
    conn.close()


def get_recent_searches(user_id=None, limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if user_id:
        c.execute("""
            SELECT github_username, mode, job_role, 
                   experience_level, total_score, searched_at
            FROM search_history
            WHERE user_id=?
            ORDER BY searched_at DESC LIMIT ?
        """, (user_id, limit))
    else:
        c.execute("""
            SELECT github_username, mode, job_role,
                   experience_level, total_score, searched_at
            FROM search_history
            ORDER BY searched_at DESC LIMIT ?
        """, (limit,))
    rows = c.fetchall()
    conn.close()
    return [
        {
            "github_username": r[0],
            "mode": r[1],
            "job_role": r[2],
            "experience_level": r[3],
            "total_score": r[4],
            "searched_at": r[5],
        }
        for r in rows
    ]


# ════════════════════════════════
# LEADERBOARD FUNCTIONS
# ════════════════════════════════
def update_leaderboard(
    github_username,
    name,
    avatar_url,
    developer_type,
    total_score,
    job_role=None,
    experience_level=None
):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO leaderboard
        (github_username, name, avatar_url, developer_type,
         total_score, job_role, experience_level)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(github_username) DO UPDATE SET
            name=excluded.name,
            avatar_url=excluded.avatar_url,
            developer_type=excluded.developer_type,
            total_score=excluded.total_score,
            job_role=excluded.job_role,
            experience_level=excluded.experience_level,
            updated_at=CURRENT_TIMESTAMP
    """, (github_username, name, avatar_url, developer_type,
          total_score, job_role, experience_level))
    conn.commit()
    conn.close()


def get_leaderboard(limit=10, job_role=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if job_role:
        c.execute("""
            SELECT github_username, name, avatar_url,
                   developer_type, total_score, job_role,
                   experience_level, updated_at
            FROM leaderboard
            WHERE job_role=?
            ORDER BY total_score DESC LIMIT ?
        """, (job_role, limit))
    else:
        c.execute("""
            SELECT github_username, name, avatar_url,
                   developer_type, total_score, job_role,
                   experience_level, updated_at
            FROM leaderboard
            ORDER BY total_score DESC LIMIT ?
        """, (limit,))
    rows = c.fetchall()
    conn.close()
    return [
        {
            "github_username": r[0],
            "name": r[1],
            "avatar_url": r[2],
            "developer_type": r[3],
            "total_score": r[4],
            "job_role": r[5],
            "experience_level": r[6],
            "updated_at": r[7],
        }
        for r in rows
    ]


# ════════════════════════════════
# NOTIFICATION FUNCTIONS
# ════════════════════════════════
def save_notification(user_id, notif_type, message):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO notifications (user_id, type, message)
        VALUES (?, ?, ?)
    """, (user_id, notif_type, message))
    conn.commit()
    conn.close()


def mark_notification_sent(notif_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        UPDATE notifications
        SET status='sent', sent_at=CURRENT_TIMESTAMP
        WHERE id=?
    """, (notif_id,))
    conn.commit()
    conn.close()


def get_pending_notifications(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, type, message, created_at
        FROM notifications
        WHERE user_id=? AND status='pending'
        ORDER BY created_at DESC
    """, (user_id,))
    rows = c.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "type": r[1],
            "message": r[2],
            "created_at": r[3],
        }
        for r in rows
    ]


# ════════════════════════════════
# STATS FUNCTIONS
# ════════════════════════════════
def get_app_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM search_history")
    total_searches = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM leaderboard")
    total_leaderboard = c.fetchone()[0]

    c.execute("""
        SELECT job_role, COUNT(*) as count
        FROM search_history
        WHERE job_role IS NOT NULL
        GROUP BY job_role
        ORDER BY count DESC LIMIT 5
    """)
    popular_roles = c.fetchall()

    conn.close()
    return {
        "total_users": total_users,
        "total_searches": total_searches,
        "total_leaderboard": total_leaderboard,
        "popular_roles": [{"role": r[0], "count": r[1]} for r in popular_roles]
    }


# ════════════════════════════════
# TEST
# ════════════════════════════════
if __name__ == "__main__":
    init_db()

    # Test user
    user_id = create_or_update_user(
        email="test@gmail.com",
        name="Test User",
        avatar_url="https://github.com/test.png",
        auth_provider="google",
        github_username="torvalds"
    )
    print(f"[OK] User created: ID {user_id}")

    # Test search history
    save_search(
        github_username="torvalds",
        mode="career",
        job_role="Backend Developer",
        experience_level="Senior",
        total_score=87.5,
        career_score=72.3,
        ats_score=65.0,
        user_id=user_id
    )
    print("[OK] Search saved!")

    # Test leaderboard
    update_leaderboard(
        github_username="torvalds",
        name="Linus Torvalds",
        avatar_url="https://github.com/torvalds.png",
        developer_type="Systems Developer",
        total_score=87.5,
        job_role="Backend Developer",
        experience_level="Senior"
    )
    print("[OK] Leaderboard updated!")

    # Stats
    stats = get_app_stats()
    print(f"\n[STATS] App Stats:")
    print(f"  Users: {stats['total_users']}")
    print(f"  Searches: {stats['total_searches']}")
    print(f"  Leaderboard: {stats['total_leaderboard']}")