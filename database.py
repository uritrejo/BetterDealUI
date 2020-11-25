import pyrebase
import traceback
import logging

firebaseConfig = {
    'apiKey': "AIzaSyCEE9JHRfzIpuxgtMzFeaZuqw2_DaFkCQY",
    'authDomain': "betterdeals-de427.firebaseapp.com",
    'databaseURL': "https://betterdeals-de427.firebaseio.com",
    'projectId': "betterdeals-de427",
    'storageBucket': "betterdeals-de427.appspot.com",
    'messagingSenderId': "33445910441",
    'appId': "1:33445910441:web:d89aecd987708ff8a916b8",
    'measurementId': "G-ZWMM7LGS70"
}


'''
    Documentation on how to use pyrebase available at:
    https://github.com/thisbejim/Pyrebase
'''

# we get the logger
logger = logging.getLogger("BetterDealUI")


def retrieveSearches():
    print("Retrieve Searches called")
    searches = []
    identifiers = []
    try:
        fire = pyrebase.initialize_app(firebaseConfig)
        db = fire.database()
        searches_json = db.child('Searches').get()
        '''
            Return a list of lists of format ['Model', 'Link']
        '''
        for search in searches_json.each():
            new_search = (search.val()['Model'], search.val()['Link'])
            searches.append(new_search)
            identifiers.append(search.key())
    except:
        # print("Error retrieving searches")
        logger.exception("Error retrieving searches: ")

    # later you could do return links, models (if ever needed for the UI)
    return searches, identifiers


def retrieveCars(filters=["","","",""], getAll=False):
    cars = []
    try:
        fire = pyrebase.initialize_app(firebaseConfig)
        db = fire.database()

        if getAll:
            cars_json = db.child('Cars').get()
        # if we have both a keyword and price ranges:
        if filters[0] != "" and filters[1] != "" and filters[2] != "":
            # filter all
            print("Filter")
        # if we only have a keyword
        elif filters[0] != "":
            # filter by keyword
            print("Filter")
        # if we only have a price range:
        elif filters[1] != "" and filters[2] != "":
            # filter by price range
            print("Filter")
        # if there are no filters
        else:
            cars_json = db.child('Cars').get()

        for car in cars_json.each():
            new_car = (car.val()['Model'], car.val()['Price'], car.val()['Date'], car.val()['Link'])
            cars.append(new_car)
    except:
        # print("Error retrieving cars from the database.")
        logger.exception("Error retrieving cars from the database:")
    return cars


def addNewSearch(link, model):
    try:
        fire = pyrebase.initialize_app(firebaseConfig)
        db = fire.database()
        search = {
            'Model': model,
            'Link': link
        }
        db.child('Searches').push(search)
    except:
        logger.exception("Error adding search.")


# removes the selected search
def removeSearch(key):
    try:
        fire = pyrebase.initialize_app(firebaseConfig)
        db = fire.database()
        db.child("Searches").child(key).remove()
    except:
        logger.exception("Error removing search.")
