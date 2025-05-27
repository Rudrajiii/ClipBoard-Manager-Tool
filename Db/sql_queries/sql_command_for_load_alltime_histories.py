SQL_LOAD_ALLTIME_HISTORY = """
SELECT content, date FROM clipboard_items
ORDER BY timestamp DESC
"""