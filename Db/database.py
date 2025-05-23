from PyQt5.QtSql import QSqlDatabase # type: ignore

def get_db_connection():
    db = QSqlDatabase.database()
    if not db.isValid():
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName("clipboard_history.db")
        if not db.open():
            print("Failed to connect to database.")
            return None
    return db