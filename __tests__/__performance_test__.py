import os
import sys
import random
import string
from datetime import datetime, timedelta
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

# Database connection setup
def get_db_connection():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("clipboard_history.db")
    if not db.open():
        print(f"Failed to connect to database: {db.lastError().text()}")
        return None
    return db

def generate_random_text(min_length=10, max_length=200):
    """Generate random text content with varying length"""
    length = random.randint(min_length, max_length)
    text_types = [
        # Regular text with words
        lambda: ' '.join(''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10))) 
                         for _ in range(length // 8)),
        # URL
        lambda: f"https://www.{''.join(random.choices(string.ascii_lowercase, k=8))}.com/{''.join(random.choices(string.ascii_lowercase, k=12))}",
        # Code snippet
        lambda: f"def function_name():\n    return '{''.join(random.choices(string.ascii_letters, k=15))}'\n\n# Comment here\nresult = function_name()",
        # JSON data
        lambda: '{\n    "id": ' + str(random.randint(1, 1000)) + ',\n    "name": "' + 
                ''.join(random.choices(string.ascii_letters, k=10)) + '",\n    "value": ' + 
                str(random.random() * 100) + '\n}'
    ]
    
    return random.choice(text_types)()

def add_test_data(today_entries=100, previous_entries=200):
    """Add test data to the database"""
    db = get_db_connection()
    if not db:
        print("Could not connect to database")
        return False
    
    print("Adding test data to database...")
    
    # Get current date
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Prepare query
    query = QSqlQuery()
    query.prepare("""
        INSERT INTO clipboard_items (content, date, timestamp) 
        VALUES (:content, :date, :timestamp)
    """)
    
    # Add today's entries
    print(f"Adding {today_entries} entries for today ({today})...")
    for i in range(today_entries):
        content = generate_random_text()
        timestamp = datetime.now() - timedelta(minutes=random.randint(1, 1440))  # Random time within last 24h
        
        query.bindValue(":content", content)
        query.bindValue(":date", today)
        query.bindValue(":timestamp", timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        
        if not query.exec_():
            print(f"Error adding entry: {query.lastError().text()}")
        
        if i % 20 == 0:
            sys.stdout.write(f"\rProgress: {i}/{today_entries}")
            sys.stdout.flush()
    
    print("\nToday's entries added successfully!")
    
    # Add previous days' entries
    print(f"Adding {previous_entries} entries for previous days...")
    for i in range(previous_entries):
        content = generate_random_text()
        days_ago = random.randint(1, 30)  # Random day in the last month
        entry_date = datetime.now() - timedelta(days=days_ago)
        date_str = entry_date.strftime("%Y-%m-%d")
        timestamp = entry_date.replace(
            hour=random.randint(0, 23),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )
        
        query.bindValue(":content", content)
        query.bindValue(":date", date_str)
        query.bindValue(":timestamp", timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        
        if not query.exec_():
            print(f"Error adding entry: {query.lastError().text()}")
        
        if i % 20 == 0:
            sys.stdout.write(f"\rProgress: {i}/{previous_entries}")
            sys.stdout.flush()
    
    print("\nPrevious days' entries added successfully!")
    print(f"Total entries added: {today_entries + previous_entries}")
    
    # Close connection
    db.close()
    return True

if __name__ == "__main__":
    # Check if database exists
    if not os.path.exists("clipboard_history.db"):
        print("Database file 'clipboard_history.db' not found!")
        sys.exit(1)
    
    print("This will add test data to your clipboard database.")
    print("- 100 entries for today")
    print("- 200 entries for previous days")
    
    confirmation = input("Continue? (y/n): ")
    if confirmation.lower() != 'y':
        print("Operation cancelled.")
        sys.exit(0)
    
    success = add_test_data(100, 200)
    
    if success:
        print("Test data added successfully!")
    else:
        print("Failed to add test data.")