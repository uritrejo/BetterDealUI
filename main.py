import csv
import sys
import logging
import logging.handlers
# import traceback
import os

from enum import Enum

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
import database as db


# we set the logger configuration to write to a file, and also to print to terminal
logger = logging.getLogger("BetterDealUI")
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(
    "logsUI.log", maxBytes=(1048576*5), backupCount=7
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())


class Items(Enum):
    SEARCHES = 0
    CARS = 1


class TableModel(QAbstractTableModel):

    def __init__(self, item_type, filters=[]):
        super().__init__()
        if item_type == Items.SEARCHES:
            self.headers = ["Model", "Link"]
            self.rows, self.row_identifiers = db.retrieveSearches()
        elif item_type == Items.CARS:
            self.headers = ["Model", "Price", "Date", "Link"]
            self.retrieveFilteredCars(filters)

    # fills in the rows according to the filters
    def retrieveFilteredCars(self, filters):
        # here do stuff with the two filters to fill in the data with the correct stuff
        # probably call an extra method

        self.rows = db.retrieveCars(filters)
        # to avoid wasting requests to the database, we'll use a dummy to test
        # self.rows = [("Honda Civic", "4000", "2020/11/23", "hondacivic.com"),
        #              ("Mini Cooper", "7750", "2020/11/25", "minicooper.com"),
        #              ("Mustang", "11286", "2020/11/24", "mustang.com")]

    def rowCount(self, parent):
        return len(self.rows)

    def columnCount(self, parent):
        return len(self.headers)

    def data(self, index, role):
        if role != Qt.DisplayRole:
            return QVariant()
        return self.rows[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return QVariant()
        return self.headers[section]


# Creating the main window
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Better Deal'
        self.left = 0
        self.top = 0
        self.width = 900
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.tab_widget = TabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.setWindowIcon(QtGui.QIcon('images/icon.png'))
        self.show()


def show_pop_up(message):
    msg = QMessageBox()
    msg.setWindowTitle("Message")
    msg.setText(message)
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setWindowIcon(QtGui.QIcon('images/icon.png'))
    # msg.setDetailedText("details")
    x = msg.exec_()


class TabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()

        # initialize additional tabs
        self.tab_search = None
        self.tab_cars = None
        self.tab_advanced = None

        # initialize the rest of the components needed
        # MAYBE WILL NEED TO BE CHANGED
        # components for search tab
        self.table_search = None
        self.table_view_search = None
        self.add_search_widget = None
        self.edit_model_search = None
        self.edit_link_search = None

        # components for cars tab
        self.table_cars = None
        self.table_view_cars = None
        self.filter_cars_widget = None
        self.edit_filter_cars = None
        self.edit_price_from = None
        self.edit_price_to = None
        self.edit_date = None

        # potentially will mess with the size:
        # self.tabs.resize(300, 200)

        # create tabs
        self.create_search_tab()
        self.create_cars_tab()
        self.create_advanced_tab()

        # Add tabs
        self.tabs.addTab(self.tab_search, "Searches")
        self.tabs.addTab(self.tab_cars, "Cars")
        self.tabs.addTab(self.tab_advanced, "Advanced")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def create_search_tab(self):
        self.tab_search = QWidget()
        self.tab_search.layout = QVBoxLayout(self)

        # create widget for adding search
        self.add_search_widget = QWidget()

        self.edit_model_search = QLineEdit()
        self.edit_link_search = QLineEdit()

        bt_add_search = QPushButton("Add Search")
        bt_add_search.setDefault(True)
        bt_add_search.clicked.connect(self.on_bt_add_search_click)

        add_search_layout = QGridLayout()
        add_search_layout.addWidget(QLabel("Model: "), 0, 0)
        add_search_layout.addWidget(self.edit_model_search, 0, 1)
        add_search_layout.addWidget(QLabel("Link: "), 0, 2)
        add_search_layout.addWidget(self.edit_link_search, 0, 3)
        add_search_layout.addWidget(bt_add_search, 0, 4)
        self.add_search_widget.setLayout(add_search_layout)

        self.tab_search.layout.addWidget(self.add_search_widget)

        # create refresh and remove buttons:

        # create widget that contains buttons
        refresh_search_widget = QWidget()
        refresh_search_layout = QGridLayout()

        # create refresh button
        bt_refresh_search = QPushButton("Refresh")
        bt_refresh_search.setDefault(True)
        bt_refresh_search.clicked.connect(self.on_bt_refresh_search_click)

        # create remove button
        bt_remove_search = QPushButton("Remove selected search(es)")
        bt_remove_search.setDefault(True)
        bt_remove_search.clicked.connect(self.on_bt_remove_search_click)

        refresh_search_layout.addWidget(bt_refresh_search, 0, 0)
        refresh_search_layout.addWidget(bt_remove_search, 0, 1)

        refresh_search_widget.setLayout(refresh_search_layout)

        self.tab_search.layout.addWidget(refresh_search_widget)

        # self.tab_search.layout.addWidget(bt_refresh_search)

        # These are self... in order to access them from the on clicks
        # create the search table
        self.table_search = TableModel(Items.SEARCHES)
        self.table_view_search = QTableView()
        self.table_view_search.setModel(self.table_search)
        self.table_view_search.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view_search.resizeColumnsToContents()
        self.table_view_search.resizeRowsToContents()
        # checa como resizearlo para que se extienda al parent

        # self.table_view.show()  # antes estaba esto tambien
        self.tab_search.layout.addWidget(self.table_view_search)

        self.tab_search.setLayout(self.tab_search.layout)

    def create_cars_tab(self):
        self.tab_cars = QWidget()
        self.tab_cars.layout = QVBoxLayout(self)

        # create widget for adding search
        self.filter_cars_widget = QWidget()

        # Aqui le puedo añadir que haga busqueda segun precio, doy un range...

        self.edit_filter_cars = QLineEdit()
        self.edit_price_from = QLineEdit()
        self.edit_price_to = QLineEdit()
        self.edit_date = QLineEdit()
        self.edit_date.setPlaceholderText("YYYY/MM/DD")

        bt_filter_cars = QPushButton("Filter Search")
        bt_filter_cars.setDefault(True)
        bt_filter_cars.clicked.connect(self.on_bt_filter_cars_click)

        filter_cars_layout = QGridLayout()
        filter_cars_layout.addWidget(QLabel("Keyword: "), 0, 0)
        filter_cars_layout.addWidget(self.edit_filter_cars, 0, 1)
        filter_cars_layout.addWidget(QLabel("Price from: "), 0, 2)
        filter_cars_layout.addWidget(self.edit_price_from, 0, 3)
        filter_cars_layout.addWidget(QLabel("to: "), 0, 4)
        filter_cars_layout.addWidget(self.edit_price_to, 0, 5)
        filter_cars_layout.addWidget(QLabel("Date: "), 0, 6)
        filter_cars_layout.addWidget(self.edit_date, 0, 7)

        filter_cars_layout.addWidget(bt_filter_cars, 0, 8)
        self.filter_cars_widget.setLayout(filter_cars_layout)

        self.tab_cars.layout.addWidget(self.filter_cars_widget)

        # These are self... in order to access them from the on clicks
        # create the search table
        self.table_cars = TableModel(Items.CARS, filters=["","","",""])
        self.table_view_cars = QTableView()
        self.table_view_cars.setModel(self.table_cars)
        self.table_view_cars.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view_cars.resizeColumnsToContents()
        self.table_view_cars.resizeRowsToContents()

        # self.table_view.show()  # antes estaba esto tambien
        self.tab_cars.layout.addWidget(self.table_view_cars)

        # we add a button to download the data in csv format
        # maybe add the option to download in json format, would be really easy to implement
        bt_download_cars = QPushButton("Download all cars to csv")
        bt_download_cars.setDefault(True)
        bt_download_cars.clicked.connect(self.on_bt_download_cars_click)
        self.tab_cars.layout.addWidget(bt_download_cars)

        self.tab_cars.setLayout(self.tab_cars.layout)

    def create_advanced_tab(self):
        self.tab_advanced = QWidget()
        self.tab_advanced.layout = QVBoxLayout(self)

        # we add a button to download the data in csv format
        # maybe add the option to download in json format, would be really easy to implement
        bt_delete_data = QPushButton("DELETE ALL CARS FROM DATABASE")
        bt_delete_data.setDefault(True)
        bt_delete_data.clicked.connect(self.on_bt_delete_cars_click)
        self.tab_advanced.layout.addWidget(bt_delete_data)
        # self.tab_advanced.layout.addWidget(QLabel("If you want to add some info")

        self.tab_advanced.setLayout(self.tab_advanced.layout)

    def on_bt_refresh_search_click(self):
        logger.info("Refresh searches ")
        self.table_search = TableModel(Items.SEARCHES)
        self.table_view_search.setModel(self.table_search)
        self.table_view_search.resizeColumnsToContents()
        self.table_view_search.resizeRowsToContents()
        show_pop_up("Searches have been refreshed.")

    def on_bt_refresh_cars_click(self):
        logger.info("Refresh Cars")
        self.table_cars = TableModel(Items.CARS, ["","","",""])
        self.table_view_cars.setModel(self.table_cars)
        self.table_view_cars.resizeColumnsToContents()
        self.table_view_cars.resizeRowsToContents()
        show_pop_up("Cars have been refreshed.")

    def on_bt_add_search_click(self):
        if self.edit_model_search.text() == "" or self.edit_link_search.text() == "":
            print("Method called with no values, no action taken")
            show_pop_up("Add was called with no values, no action taken")
            return
        logger.info("Add search: " + self.edit_model_search.text() + " / " + self.edit_link_search.text())
        db.addNewSearch(self.edit_link_search.text(), self.edit_model_search.text())
        # we update the table by faking a click on refresh
        self.on_bt_refresh_search_click()
        self.edit_link_search.setText("")
        self.edit_model_search.setText("")

    def on_bt_remove_search_click(self):
        # print("Selection: ", self.table_view_search.selectionModel().selectedRows())
        selected_rows = self.table_view_search.selectionModel().selectedRows()
        for i in range(len(selected_rows)):
            index_to_remove = selected_rows[i].row()
            # print("Index of row: ", index_to_remove)
            # print(self.table_search.rows[index_to_remove])
            logger.info("Remove search called on " + str(self.table_search.rows[index_to_remove]))
            db.removeSearch(self.table_search.row_identifiers[index_to_remove])
        self.on_bt_refresh_search_click()

    def on_bt_filter_cars_click(self):

        filters = [self.edit_filter_cars.text(), self.edit_price_from.text(),
                   self.edit_price_to.text(), self.edit_date.text()]
        logger.info("Filter cars called with values: " + str(filters))

        # we make sure the filters are valid:
        if filters[0] == filters[1] == filters[2] == filters[3] == "":
            show_pop_up("Filters empty")
        else:
            # if the price range is incomplete
            if (filters[1] != "" and filters[2] == "") or (filters[1] == "" and filters[2] != ""):
                # we set both values to null to avoid errors in the filters
                filters[1] = ""
                filters[2] = ""
                show_pop_up("Price range incomplete, ignoring price ranges." +
                            "Please fill in 'to' and 'from' to see results.")

            # if we still have the price range values, we make sure they can be parsed to double
            if filters[1] != "" and filters[2] != "":
                try:  # we just want to know if it is possible
                    float(self.edit_price_from.text())
                    float(self.edit_price_to.text())
                except:
                    # we set them to an empty string to avoid errors
                    filters[1] = ""
                    filters[2] = ""
                    logger.exception("Unable to parse price value to float.")
                    show_pop_up("Provided price values were invalid. Values must be numeric.")

            # if we have a date included
            if filters[3] != "":
                if len(filters[3]) == 10:
                    try:
                        for c in range(len(filters[3])):
                            if c != 4 and c != 7:
                                int(filters[3][c])
                            else:
                                if filters[3][c] != '/':
                                    raise Exception
                    except:
                        filters[3] = ""
                        logger.exception("Invalid date format.")
                        show_pop_up("Invalid date format. Please revise.")
                else:
                    filters[3] = ""
                    show_pop_up("Invalid date format. Please revise.")

        self.table_cars = TableModel(Items.CARS, filters)
        self.table_view_cars.setModel(self.table_cars)
        self.table_view_cars.resizeColumnsToContents()
        self.table_view_cars.resizeRowsToContents()

        show_pop_up("Displaying at most 200 cars from filtered search: Keyword: " + filters[0] +
                    ", Price from " + filters[1] + " to " + filters[2] + ", Date: " + filters[3])

        # show_pop_up("NOT IMPLEMENTED YET")

    # will write the collected cars into a csv file (cars.csv, in current directory)
    def on_bt_download_cars_click(self):
        # writes the collected cars into a csv file (excluding the links, might change later)

        cars = db.retrieveCars(getAll=True)
        # could also be only retrieving the ones that are in the search at the moment

        # for testing purposes:
        # cars = [("Honda Civic", "4000", "2020/11/23", "hondacivic.com"),
        #              ("Mini Cooper", "7750", "2020/11/25", "minicooper.com"),
        #              ("Mustang", "11286", "2020/11/24", "mustang.com")]

        if len(cars) == 0:
            logger.info("List of cars was empty or an error occurred. No file has been created.")
            show_pop_up("List of cars was empty or an error occurred. No file has been created.")
            return

        try:
            with open('cars.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Model", "Price", "Date", "Link"])
                for i in range(len(cars)):
                    # the encoding is to avoid issues we were having with some characters
                    car_formatted = [cars[i][0].encode('utf-8').decode('utf-8'),  # model
                                     cars[i][1],  # price
                                     cars[i][2].encode('utf-8').decode('utf-8'),  # date
                                     cars[i][3].encode('utf-8').decode('utf-8')]   # link
                    writer.writerow(car_formatted)
                currentDirectory = os.getcwd()
                show_pop_up("Cars were downloaded to " + str(currentDirectory) + "\\cars.csv")
        except:
            show_pop_up("Failed to download cars.")
            logger.exception("Failed to download cars: ")

    def on_bt_delete_cars_click(self):
        logger.warning("ALL CARS TO BE DELETED FROM DB")
        db.deleteAllCars()
        show_pop_up("Cars have been deleted from database.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
