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
        logger.error("Error retrieving searches: " + traceback.print_exc())

    # later you could do return links, models (if ever needed for the UI)
    return searches, identifiers


def retrieveCars():
    cars = []
    try:
        fire = pyrebase.initialize_app(firebaseConfig)
        db = fire.database()
        cars_json = db.child('Cars').get()
        for car in cars_json.each():
            new_car = (car.val()['Model'], car.val()['Price'], car.val()['Date'], car.val()['Link'])
            cars.append(new_car)
    except:
        # print("Error retrieving cars from the database.")
        logger.error("Error retrieving cars from the database:" + traceback.print_exc())
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
        logger.error("Error adding search." + traceback.print_exc())


# removes the selected search
def removeSearch(key):
    try:
        fire = pyrebase.initialize_app(firebaseConfig)
        db = fire.database()
        db.child("Searches").child(key).remove()
    except:
        logger.error("Error removing search." + traceback.print_exc())
