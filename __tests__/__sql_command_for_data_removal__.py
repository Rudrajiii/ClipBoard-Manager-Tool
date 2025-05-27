from PyQt5.QtSql import QSqlDatabase, QSqlQuery  # type: ignore
from datetime import datetime
from pytz import timezone
import os

os.makedirs("logs", exist_ok=True)

def get_test_db_connection():
    # Use a unique connection name to avoid conflicts
    connection_name = "cleanup_connection"
    
    # Remove existing connection if it exists
    if QSqlDatabase.contains(connection_name):
        QSqlDatabase.removeDatabase(connection_name)
    
    db = QSqlDatabase.addDatabase('QSQLITE', connection_name)
    
    # Use absolute path or check if the database exists
    db_path = os.path.abspath("clipboard_history.db")  # Changed from "../clipboard_history.db"
    
    # Check if database file exists
    if not os.path.exists(db_path):
        print(f"❌ Database file not found at: {db_path}")
        return None
    
    db.setDatabaseName(db_path)
    
    if not db.open():
        print("❌ Failed to connect to database:", db.lastError().text())
        return None
    
    print(f"✅ Connected to database: {db_path}")
    return db

def check_table_exists(db):
    """Check if clipboard_items table exists"""
    query = QSqlQuery(db)
    success = query.exec_("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='clipboard_items'
    """)
    
    if success and query.next():
        return True
    return False

def clear_today_from_db():
    db = get_test_db_connection()
    if not db:
        return False
    
    try:
        # Check if table exists
        if not check_table_exists(db):
            print("❌ Table 'clipboard_items' does not exist in the database")
            log_operation("DELETE", "FAILURE - TABLE NOT FOUND")
            return False
        
        query = QSqlQuery(db)
        
        # First, let's see what tables exist
        print("📋 Available tables in database:")
        table_query = QSqlQuery(db)
        table_query.exec_("SELECT name FROM sqlite_master WHERE type='table'")
        while table_query.next():
            print(f"   - {table_query.value(0)}")
        
        # Check current entries for today
        check_query = QSqlQuery(db)
        check_success = check_query.exec_("""
            SELECT COUNT(*) FROM clipboard_items 
            WHERE date = DATE('now', 'localtime')
        """)
        
        if check_success and check_query.next():
            count = check_query.value(0)
            print(f"📊 Found {count} entries for today")
            if count == 0:
                print("ℹ️  No entries to delete for today")
                log_operation("DELETE", "SUCCESS - NO ENTRIES")
                return True
        
        # Perform the deletion
        success = query.exec_("""
            DELETE FROM clipboard_items
            WHERE date = DATE('now', 'localtime')
        """)
        
        if success:
            rows_affected = query.numRowsAffected()
            print(f"✅ Successfully deleted {rows_affected} today's entries")
            log_operation("DELETE", f"SUCCESS - {rows_affected} ROWS DELETED")
            return True
        else:
            error_msg = query.lastError().text()
            print(f"❌ Failed to delete: {error_msg}")
            log_operation("DELETE", f"FAILURE - {error_msg}")
            return False
    
    finally:
        # Always close the database connection
        if db.isOpen():
            db.close()
        QSqlDatabase.removeDatabase("cleanup_connection")

def log_operation(operation, status):
    """Log operation with proper formatting"""
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    with open("logs/test_logs.txt", "a", encoding='utf-8') as log_file:
        log_file.write(f"Operation: {operation}\n")
        log_file.write(f"Triggered at: {ind_time}\n")
        log_file.write(f"Status: {status}\n")
        log_file.write("-" * 50 + "\n\n")

def show_database_info():
    """Show information about the database"""
    db = get_test_db_connection()
    if not db:
        return
    
    print("\n📁 Database Information:")
    print(f"   Database file: {db.databaseName()}")
    
    # Show all tables
    query = QSqlQuery(db)
    query.exec_("SELECT name FROM sqlite_master WHERE type='table'")
    print("   Tables:")
    while query.next():
        table_name = query.value(0)
        print(f"     - {table_name}")
        
        # Show table structure
        structure_query = QSqlQuery(db)
        structure_query.exec_(f"PRAGMA table_info({table_name})")
        print(f"       Columns:")
        while structure_query.next():
            col_name = structure_query.value(1)
            col_type = structure_query.value(2)
            print(f"         • {col_name} ({col_type})")
    
    # Close the database connection properly
    db.close()
    QSqlDatabase.removeDatabase("cleanup_connection")

if __name__ == "__main__":
    print("🧹 Clipboard History Cleanup Tool")
    print("=" * 40)
    
    # Show database info first
    show_database_info()
    
    print("\n🔄 Starting cleanup process...")
    success = clear_today_from_db()
    
    if success:
        print("\n✅ Cleanup completed successfully!")
    else:
        print("\n❌ Cleanup failed!")
        print("\n🔍 Troubleshooting tips:")
        print("   1. Check if clipboard_history.db exists in the current directory")
        print("   2. Verify the database contains the 'clipboard_items' table")
        print("   3. Make sure the database file is not corrupted")
        print("   4. Check if another process is using the database")