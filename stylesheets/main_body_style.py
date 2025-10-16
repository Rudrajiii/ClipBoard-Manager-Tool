SCROLL_AREA_STYLE = """
        QScrollArea {
                border: none;
                background-color: rgb(26, 26, 26);
        }
        """

SCROLL_BAR_STYLE = """
        QScrollBar:vertical {
                background-color: rgb(41, 41, 41);
                width: 12px;
                border-radius: 6px;
                margin: 0px 0px 0px 0px;
                padding: 2px;
        }
        QScrollBar::handle:vertical {
                background-color: rgb(75, 75, 75);
                border-radius: 6px;
                min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
                background-color: rgb(100, 100, 100);
        }
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
                background: none;
                border: none;
                height: 0px;
        }
        """

CONTENT_WIDGET_STYLE = """
background-color: #252525;
"""

