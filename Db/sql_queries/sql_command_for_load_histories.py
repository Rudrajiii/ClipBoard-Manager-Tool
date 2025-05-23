def SQL_QUERY_FOR_LOAD_HISTORIES(today_date):
    """
    SQL query to load histories from the database.
    """
    return f"""
            SELECT content FROM clipboard_items
            WHERE date = '{today_date}'
            ORDER BY timestamp ASC
    """
