import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import datetime

# Initialize Flask app
app = Flask(__name__)

# Database file name
DATABASE = 'expenses.db'

# Function to get a database connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Access columns by name
    return conn

# Function to initialize the database and create tables if they don't exist
def init_db():
    with app.app_context(): # Use application context for database operations
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()
        db.close()

# Ensure database is initialized when the app starts
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Handle POST request for adding a new expense
    if request.method == 'POST':
        description = request.form['description']
        amount_str = request.form['amount']
        
        # Basic validation
        if not description or not amount_str:
            # In a real app, you'd flash a message to the user
            return redirect(url_for('index'))

        try:
            amount = float(amount_str)
            if amount <= 0:
                # Amount must be positive
                return redirect(url_for('index')) # Or show an error
        except ValueError:
            # Invalid amount format
            return redirect(url_for('index')) # Or show an error

        db = get_db()
        db.execute('INSERT INTO expenses (description, amount) VALUES (?, ?)', (description, amount))
        db.commit()
        db.close()
        return redirect(url_for('index')) # Redirect to clear form and show updated list

    # Handle GET request to display expenses
    db = get_db()
    expenses_cursor = db.execute('SELECT id, description, amount, created_at FROM expenses ORDER BY created_at DESC')
    expenses = expenses_cursor.fetchall()
    
    total_expenses_cursor = db.execute('SELECT SUM(amount) as total FROM expenses')
    total_row = total_expenses_cursor.fetchone()
    total_expenses = total_row['total'] if total_row and total_row['total'] is not None else 0.0
    
    db.close()
    
    current_year = datetime.date.today().year
    return render_template('index.html', expenses=expenses, total_expenses=total_expenses, current_year=current_year)

# Route to delete an expense
@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    db = get_db()
    db.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    db.commit()
    db.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # For development: app.run(debug=True, port=9000)
    # For production, use a WSGI server like Gunicorn as configured in startup.sh
    app.run(host='0.0.0.0', port=9000, debug=True)
