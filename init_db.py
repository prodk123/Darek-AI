#!/usr/bin/env python3
"""
Simple database initialization script for Darek AI
"""

import sqlite3
import os

def create_database():
    """Create the database with the correct schema"""
    db_path = os.path.join('instance', 'darek_ai.db')
    
    # Create instance directory if it doesn't exist
    os.makedirs('instance', exist_ok=True)
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Removed existing database")
    
    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(150) UNIQUE NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            password_hash VARCHAR(128)
        )
    ''')
    
    # Create reminders table with correct column names
    cursor.execute('''
        CREATE TABLE reminder (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task VARCHAR(300) NOT NULL,
            remind_at DATETIME NOT NULL,
            completed BOOLEAN DEFAULT 0,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
    
    # Create timers table
    cursor.execute('''
        CREATE TABLE timer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            duration INTEGER NOT NULL,
            start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            active BOOLEAN DEFAULT 1,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
    
    # Create shopping_item table with correct column names
    cursor.execute('''
        CREATE TABLE shopping_item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name VARCHAR(100) NOT NULL,
            completed BOOLEAN DEFAULT 0,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
    
    # Create notes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
    
    # Create todo_item table
    cursor.execute('''
        CREATE TABLE todo_item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task VARCHAR(200) NOT NULL,
            priority VARCHAR(20) DEFAULT 'medium',
            completed BOOLEAN DEFAULT 0,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
    
    # Create command_history table
    cursor.execute('''
        CREATE TABLE command_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command VARCHAR(500) NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            success BOOLEAN DEFAULT 1,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("Database created successfully!")
    print("Tables created: user, reminder, timer, shopping_item, todo_item, command_history")

if __name__ == "__main__":
    create_database()
