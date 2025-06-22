# expense_tracker.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Connect to SQLite database
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
""")
conn.commit()

# Add expense
def add_expense(date, category, amount, description):
    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                   (date, category, amount, description))
    conn.commit()

# View all expenses
def view_expenses():
    df = pd.read_sql("SELECT * FROM expenses", conn)
    print(df)

# Generate report
def generate_report():
    df = pd.read_sql("SELECT * FROM expenses", conn)
    if df.empty:
        print("No expenses to show.")
        return
    
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')

    summary = df.groupby(['month', 'category'])['amount'].sum().unstack().fillna(0)
    print("\n--- Monthly Expense Report ---")
    print(summary)

    summary.plot(kind='bar', stacked=True)
    plt.title('Monthly Expense Breakdown')
    plt.ylabel('Amount')
    plt.tight_layout()
    plt.show()

# Main CLI loop
def main():
    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Generate Report")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            date = input("Date (YYYY-MM-DD): ")
            category = input("Category: ")
            amount = float(input("Amount: "))
            description = input("Description: ")
            add_expense(date, category, amount, description)
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            generate_report()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

    conn.close()

if __name__ == "__main__":
    main()
