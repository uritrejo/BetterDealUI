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

# since we don't want to download crazy amounts of data every time
MAX_QUERY_SIZE = 200


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
        else:  # we look through the filters
            keyword = filters[0]
            price_from = filters[1]
            price_to = filters[2]
            date = filters[3]
            additional_price_filter = False

            if price_from != "" and price_to != "" and date != "":  # if prices and dates have been filtered
                # since firebase only allows us to query a single field at a time, we'll get the results of a given day,
                # then when adding the cars to the list, we'll only add those that fit our price range.
                cars_json = db.child("Cars").order_by_child("Date").equal_to(date).limit_to_first(MAX_QUERY_SIZE).get()
                additional_price_filter = True
            elif price_from != "" and price_to != "":  # if we only have a price range:
                # filter by price range
                cars_json = db.child("Cars").order_by_child("Price").start_at(int(price_from)).\
                    end_at(int(price_to)).limit_to_first(MAX_QUERY_SIZE).get()
            elif date != "":  # if we only have a date
                # filter by date
                cars_json = db.child("Cars").order_by_child("Date").equal_to(date).limit_to_first(MAX_QUERY_SIZE).get()
            # if there are no filters (that can be queried, keyword doesn't count)
            else:
                cars_json = db.child("Cars").order_by_child("Date").limit_to_last(MAX_QUERY_SIZE).get()

        # here we add the values into a formatted list and we perform the additional filters
        for car in cars_json.each():
            new_car = (car.val()['Model'], car.val()['Price'], car.val()['Date'], car.val()['Link'])
            # This will be our way of filtering for the keyword
            passes_filter = True
            if not getAll:
                if keyword != "":  # if we must filter by keyword
                    if keyword.casefold() not in new_car[0].casefold():  # if it is not in the model
                        passes_filter = False
                if additional_price_filter:  # if we must filter by price again
                    if new_car[1] < int(price_from) or new_car[1] > int(price_to):
                        passes_filter = False
            if passes_filter:  # if it passes all filters, we add the new car to the list
                cars.append(new_car)
    except:
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
