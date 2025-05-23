from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery # type: ignore

def init_db():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName("clipboard_history.db")
    
    if not db.open():
        print("Could not open database")
        return False

    query = QSqlQuery()
    query.exec_("""
        CREATE TABLE IF NOT EXISTS clipboard_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            date TEXT NOT NULL
        )
    """)

    return True