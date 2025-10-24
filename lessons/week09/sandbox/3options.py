#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple menu-driven DBMS for the Rick & Morty SQLite database.
- Connects to rickmorty.sqlite3 (created by build_DB.txt)
- Supports: listing tables, showing schema, running SELECT,
  and basic INSERT/UPDATE/DELETE with prompts.
"""

import sqlite3

name_str = "hz"

DB_FILE = "myCampusDB.sqlite3"

def connect():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def list_tables(conn):
    results = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    rows = results.fetchall()
    if not rows:
        print("(no tables found)")
    else:
        print("Tables:")
        for r in rows:
            print("  -", r[0])

def show_schema(conn, table=None):
        results = conn.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        for row in results.fetchall():
            print(row["sql"])
            print()

# ---------- Added helpers for running SELECT ----------
def collect_sql():
    print("Enter a SELECT statement (end with semicolon ';'):")
    buf = [] # creates an empty list in Python — it’s short for “buffer,” meaning a temporary place to store data.
    while True:
        line = input("sql> ")
        buf.append(line)
        if ";" in line:
            break
    return "\n".join(buf)

def run_select(conn):
    sql = collect_sql()
    if not sql.strip().lower().startswith("select"): # removes extra spaces (and line breaks) from the beginning and end of a string.
        print("Only SELECT statements are allowed here.")
        return
    try:
        results = conn.execute(sql) # ! the sqlite3 library sends the SQL text you typed (like SELECT * FROM Characters;) directly to the SQLite engine.
        rows = results.fetchall()
        if not rows:
            print("(no rows)")
        else:
            for row in rows:
                print(tuple(row))  # simple tuple output
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
# ------------------------------------------------------

def main():
    print("\nHi,", name_str, "! Simple DBMS loaded.\n")
    conn = connect()
    while True:
        print("\nMenu:")
        print("  1) List tables")
        print("  2) Show schema")
        print("  3) Run SELECT")
        print("  q) Quit")
        choice = input("Choose (1-3 or q): ").strip().lower()

        if choice == "1":
            list_tables(conn)
        elif choice == "2":
            show_schema(conn)
        elif choice == "3":
            run_select(conn)
        elif choice == "q":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
