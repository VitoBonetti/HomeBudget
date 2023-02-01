import re
import datetime

# queries

CREATE_SUPPLIER_TABLE = "CREATE TABLE suppliers(name TEXT NOT NULL UNIQUE);"
CREATE_PURCHASE_TABLE = """
                        CREATE TABLE purchases (
                        purchased_on TEXT NOT NULL,
                        supplier TEXT NOT NULL,
                        amout_9 REAL,
                        amount_21 REAL,
                        statigeld REAL,
                        discount REAL,
                        amount_tot REAL NOT NULL,
                        );
                        """
INSERT_NEW_SUPPLIER = "INSERT INTO suppliers VALUES (:name);"
SHOW_ALL_SUPPLIERS = "SELECT * FROM suppliers ORDER BY name;"

# constants
# get the current date to feed the calendar with

current_date = datetime.date.today()
current_year = current_date.year
current_month = current_date.month
current_day = current_date.day

# re string for check no special characters are used
string_pattern = re.compile('[@_!#$%^&*()<>?/\\|}{~:.,;\-+"\']')

# other constants

TITLE = "Home Budget"
VERSION = "v 0.1"
BOLD_TEXT = ("", 9, "bold")
TITLE_TEXT = ("", 12, "bold")
NORMAL_TEXT = ("", 9)
FORM_TEXT = ("", 8)
TREEVIEW_BG = "#EEEEEE"
TREEVIEW_SELECTED_BG = "#FAE664"

