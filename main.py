import sys

from enum import Enum
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from database import *


class Items(Enum):
    SEARCHES = 0
    CARS = 1


class TableModel(QAbstractTableModel):

    def __init__(self, item_type):
        super().__init__()
        if item_type == Items.SEARCHES:
            self.headers = ["Model", "Link"]
            self.rows = retrieveSearches()
        elif item_type == Items.CARS:
            self.headers = ["Model", "Price", "Link"]
            # self.rows = retrieveCars()
            # to avoid wasting requests to the database, we'll use a dummy for now
            self.rows = [("Honda Civic", "4000", "hondacivic.com"),
                        ("Mini Cooper", "7750", "minicooper.com"),
                        ("Mustang", "11286", "mustang.com")]

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

        self.show()


class TabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()

        # initialize additional tabs
        self.tab_search = None
        self.tab_cars = None

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

        # potentially will mess with the size:
        # self.tabs.resize(300, 200)

        # create tabs
        self.create_search_tab()
        self.create_cars_tab()

        # Add tabs
        self.tabs.addTab(self.tab_search, "Searches")
        self.tabs.addTab(self.tab_cars, "Cars")

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

        # create refresh and remove buttons

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

        # I think Imma leave this one out for now, don't see the point of loading them all
        # # create refresh button
        # bt_refresh_cars = QPushButton("Refresh")
        # bt_refresh_cars.setDefault(True)
        # bt_refresh_cars.clicked.connect(self.on_bt_refresh_cars_click)
        # self.tab_cars.layout.addWidget(bt_refresh_cars)


        # create widget for adding search
        self.filter_cars_widget = QWidget()

        # Aqui le puedo añadir que haga busqueda segun precio, doy un range...

        self.edit_filter_cars = QLineEdit()
        self.edit_price_from = QLineEdit()
        self.edit_price_to = QLineEdit()

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

        filter_cars_layout.addWidget(bt_filter_cars, 0, 6)
        self.filter_cars_widget.setLayout(filter_cars_layout)

        self.tab_cars.layout.addWidget(self.filter_cars_widget)

        # These are self... in order to access them from the on clicks
        # create the search table
        self.table_cars = TableModel(Items.CARS)
        self.table_view_cars = QTableView()
        self.table_view_cars.setModel(self.table_cars)
        self.table_view_cars.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view_cars.resizeColumnsToContents()
        self.table_view_cars.resizeRowsToContents()

        # self.table_view.show()  # antes estaba esto tambien
        self.tab_cars.layout.addWidget(self.table_view_cars)

        # we add a button to download the data in csv format
        # maybe add the option to download in json format, would be really easy to implement
        bt_download_cars = QPushButton("Download cars to csv")
        bt_download_cars.setDefault(True)
        bt_download_cars.clicked.connect(self.on_bt_download_cars)
        self.tab_cars.layout.addWidget(bt_download_cars)

        self.tab_cars.setLayout(self.tab_cars.layout)

    def on_bt_refresh_search_click(self):
        print("Refresh searches ")

        self.table_search = TableModel(Items.SEARCHES)
        self.table_view_search.setModel(self.table_search)
        self.table_view_search.resizeColumnsToContents()
        self.table_view_search.resizeRowsToContents()

    def on_bt_refresh_cars_click(self):
        print("Refresh Cars")

        self.table_cars = TableModel(Items.CARS)
        self.table_view_cars.setModel(self.table_cars)
        self.table_view_cars.resizeColumnsToContents()
        self.table_view_cars.resizeRowsToContents()

    def on_bt_add_search_click(self):
        print("Add search")
        print(self.edit_model_search.text())
        print(self.edit_link_search.text())

        # Here you can call on_bt_refresh para que se actualize la lista

    def on_bt_remove_search_click(self):
        print("Remove search")
        # print("Selection: ", self.table_view_search.selectionModel().selectedRows())
        selecte_rows = self.table_view_search.selectionModel().selectedRows()
        for i in range(len(selecte_rows)):
            print("Index of row: ", selecte_rows[i].row())

        # Here you can call on_bt_refresh para que se actualize la lista

    def on_bt_filter_cars_click(self):
        print("Filter cars")
        print(self.edit_filter_cars.text())
        print("Price from: ", self.edit_price_from.text(), " to: ", self.edit_price_to.text())

    def on_bt_download_cars(self):
        print("Downloading cars...")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
