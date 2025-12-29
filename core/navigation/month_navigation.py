from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel # type: ignore
from PyQt5 import QtWidgets # type: ignore
from PyQt5.QtCore import Qt # type: ignore
from PyQt5.QtGui import QCursor # type: ignore
from PyQt5.QtSql import QSqlQuery # type: ignore
import calendar
from datetime import date, datetime
from Db.database import *
from stylesheets.label_text_style import DATA_TEXT_FIELD_STYLE
from utils.clippad_text_resize import ElidedLabel


class MonthNavigator:
    def __init__(self, parent):
        self.parent = parent
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self.month_label = None
        self.prev_month_btn = None
        self.next_month_btn = None
        self.calendar_widget = None

    def get_days_with_data(self):
        """Get a set of days that have clipboard history data for current month/year"""
        db = get_db_connection()
        if not db:
            return set()
        
        query = QSqlQuery()
        query.prepare("""
            SELECT DISTINCT CAST(strftime('%d', date) AS INTEGER) as day
            FROM clipboard_items
            WHERE strftime('%Y', date) = :year
            AND strftime('%m', date) = :month
        """)
        query.bindValue(":year", str(self.current_year))
        query.bindValue(":month", f"{self.current_month:02d}")
        
        days_with_data = set()
        if query.exec_():
            while query.next():
                day = query.value(0)
                if day:
                    days_with_data.add(day)
        
        return days_with_data

    def load_previous_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_month_label()
        self.refresh_calendar_view()

    def load_next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_month_label()
        self.refresh_calendar_view()

    def update_month_label(self):
        from calendar import month_name
        month_str = month_name[self.current_month]
        if self.month_label:
            self.month_label.setText(f"{month_str[:3]} {self.current_year}")

    def refresh_calendar_view(self):
        """Clear and regenerate calendar buttons"""
        if hasattr(self.parent, 'calendar_widget') and self.parent.calendar_widget is not None:
            layout = self.parent.content_layout
            layout.removeWidget(self.parent.calendar_widget)
            self.parent.calendar_widget.deleteLater()
            self.parent.calendar_widget = None

        # Regenerate new calendar
        self.parent.calendar_widget = self.create_calendar_buttons()
        self.parent.content_layout.insertWidget(2, self.parent.calendar_widget)

    def create_calendar_buttons(self):
        """Create circular day buttons wrapped in a grid layout"""
        
        self.calendar_widget = QWidget(self.parent.content_widget)
        layout = QGridLayout(self.calendar_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        num_days = calendar.monthrange(self.current_year, self.current_month)[1]
        today = date.today()
        max_columns = 7
        row, col = 0, 0
        
        # Get days that have clipboard data
        days_with_data = self.get_days_with_data()

        for day in range(1, num_days + 1):
            is_today = (
                day == today.day and
                self.current_month == today.month and
                self.current_year == today.year
            )
            has_data = day in days_with_data
            
            # Determine styling based on conditions
            if is_today:
                border_style = '2px solid #34D399'
                bg_color = '#4ade80' if has_data else '#3d3a3a'
            elif has_data:
                border_style = 'none'
                bg_color = '#22c55e'
            else:
                border_style = 'none'
                bg_color = '#3d3a3a'

            btn = QPushButton(str(day))
            btn.setFixedSize(40, 40)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg_color};
                    border-radius: 20px;
                    font: 10pt "MS Shell Dlg 2";
                    color: white;
                    border: {border_style};
                }}
                QPushButton:hover {{
                    background-color: #16a34a;
                }}
                QPushButton:pressed {{
                    background-color: #15803d;
                }}
            """)
            btn.clicked.connect(lambda checked, d=day: self.load_history_for_date(d))
            layout.addWidget(btn, row, col)
            col += 1
            if col >= max_columns:
                col = 0
                row += 1

        return self.calendar_widget

    def load_history_for_date(self, day):
        print("this is indeed for testing purposes" , self.parent.is_history_button_clicked)
        target_date = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
        print(f"Loading history for {target_date}")

        # Add an attribute to keep track of the date view state
        if not hasattr(self, 'date_view_active'):
            self.date_view_active = False

        # Safely clean up previous widgets with better error handling
        def safe_remove_widget(widget_attr):
            try:
                if hasattr(self.parent, widget_attr):
                    widget = getattr(self.parent, widget_attr)
                    if widget is not None and not widget.isVisible() == False:
                        self.parent.content_layout.removeWidget(widget)
                        widget.deleteLater()
                        setattr(self.parent, widget_attr, None)
            except RuntimeError:
                # Widget already deleted, just reset the reference
                setattr(self.parent, widget_attr, None)
        
        # First, clean up everything else to make room for date content
        safe_remove_widget('clipboard_container')
        safe_remove_widget('month_nav_widget')
        safe_remove_widget('history_heading')
        safe_remove_widget('calendar_widget')
        
        self.parent.history_button.setText("Back")
        self.date_view_active = True
        
        # Create a clean container for the date view
        self.parent.clipboard_container = QtWidgets.QWidget(self.parent.content_widget)
        self.parent.clipboard_container.setObjectName("clipboard_container")
        self.parent.clipboard_container.setStyleSheet("background-color: transparent;")

        container_layout = QtWidgets.QVBoxLayout(self.parent.clipboard_container)
        container_layout.setSpacing(5)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add a date heading
        date_heading = QtWidgets.QLabel(f"Clipboard History Of {target_date}", self.parent.clipboard_container)
        date_heading.setObjectName("date_heading")
        date_heading.setStyleSheet("""
            QLabel#date_heading {
                font: 11pt "MS Shell Dlg 2";
                color: white;
                background-color: transparent;
                margin-bottom: 10px;
                color: #34D399;
            }
        """)
        container_layout.addWidget(date_heading)

        # Add the container to the main layout
        self.parent.content_layout.insertWidget(0, self.parent.clipboard_container)
        self.parent.clipboard_container_layout = container_layout

        # Now query and add items
        db = get_db_connection()
        if not db:
            return

        query = QSqlQuery()
        success = query.exec_(f"""
            SELECT content FROM clipboard_items
            WHERE date = '{target_date}'
            ORDER BY timestamp ASC
        """)

        if not success:
            print("Query failed:", query.lastError().text())
            return

        # Reset temporary list for current view
        if hasattr(self.parent, 'current_view_items'):
            self.parent.current_view_items.clear()
        else:
            self.parent.current_view_items = []

        count = 0
        while query.next():
            text = query.value(0)
            self.parent.current_view_items.append(text)
            
            # Add item to UI
            label = ElidedLabel(manager=self.parent, parent=self.parent.clipboard_container)
            label.setOriginalText(text)
            label.setMaxLines(3)
            label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            label.setWordWrap(True)
            label.setCursor(Qt.PointingHandCursor)
            label.setStyleSheet(DATA_TEXT_FIELD_STYLE)
            label.setObjectName("dynamic_text_label")
            label.setMinimumHeight(40)
            
            # Add to container layout
            self.parent.clipboard_container_layout.addWidget(label)
            count += 1
            
        # Show a message if no items found
        if count == 0:
            no_items_label = QtWidgets.QLabel(f"No clipboard items found for {target_date}", self.parent.clipboard_container)
            no_items_label.setAlignment(Qt.AlignCenter)
            no_items_label.setStyleSheet("color: #888; font-size: 16px; padding: 20px;")
            self.parent.clipboard_container_layout.addWidget(no_items_label)
