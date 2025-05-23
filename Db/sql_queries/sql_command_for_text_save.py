SQL_CHECK_FOR_TEXT_SAVE = """
    SELECT COUNT(*) FROM clipboard_items WHERE content = :content AND date = :date
    """