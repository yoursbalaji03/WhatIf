import os
import sqlite3

DATABASE = os.path.join("/tmp", "whatif.db")


def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            decision TEXT NOT NULL,
            savings REAL NOT NULL,
            income REAL NOT NULL,
            expenses REAL NOT NULL,
            cost REAL NOT NULL,
            months INTEGER NOT NULL,
            recommendation TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_simulation(
    decision,
    savings,
    income,
    expenses,
    cost,
    months,
    recommendation
):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO simulations
        (decision, savings, income, expenses, cost, months, recommendation)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        decision,
        savings,
        income,
        expenses,
        cost,
        months,
        recommendation
    ))

    connection.commit()
    connection.close()


def get_simulations():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM simulations
        ORDER BY id DESC
    """)

    simulations = cursor.fetchall()

    connection.close()

    return simulations
