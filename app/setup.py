"""
Van Nguyen
Tradeshift Mid level coding exercise.
6/15/2020
filename: setup.py
"""

import sqlite3
from abstract_database_connection import AbstractDatabaseConnection

create_statements = {
    # Create statement for node table.
    'node_table_sql' : """CREATE TABLE IF NOT EXISTS node (
        name TEXT NOT NULL,
        parent_name TEXT NULLABLE,
        root_name TEXT,
        height INTEGER,
        is_current TINYINT(1) DEFAULT 1
    );"""
}

insert_statements = {
    # Insert statement for album table.
    'node_insert_sql' : """INSERT INTO node(name, parent_name, root_name, height) VALUES
        ("root", "NULL", "root", 0),
        ("a", "root", "root", 1),
        ("b", "root", "root", 1),
        ("c", "a", "root", 2)
    ;"""
}

def create_tables():
    """
    Creates all table in the database.
    """
    with AbstractDatabaseConnection('amazingco.db') as conn:
        cursor = conn.cursor()
        for cs in create_statements:
            cursor.execute(create_statements[cs])
        conn.commit()

def seed():
    """
    Insert sample data to table in the database.
    """
    with AbstractDatabaseConnection('amazingco.db') as conn:
        cursor = conn.cursor()
        for ins in insert_statements:
            cursor.execute(insert_statements[ins])
        conn.commit()

def setup():
    """
    Create and seed the database.
    """
    create_tables()
    seed()

if __name__ == '__main__':
    setup()