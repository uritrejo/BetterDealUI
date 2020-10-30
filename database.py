import uuid
import pyrebase


firebaseConfig = {
    'apiKey': "AIzaSyCEE9JHRfzIpuxgtMzFeaZuqw2_DaFkCQY",
    'authDomain': "betterdeals-de427.firebaseapp.com",
    'databaseURL': "https://betterdeals-de427.firebaseio.com",
    'projectId': "betterdeals-de427",
    'storageBucket': "betterdeals-de427.appspot.com",
    'messagingSenderId': "33445910441",
    'appId': "1:33445910441:web:d89aecd987708ff8a916b8",
    'measurementId': "G-J3PE7FMQ4M"
}


'''
    Documentation on how to use pyrebase available at:
    https://github.com/thisbejim/Pyrebase
'''

def retrieveSearches():
    print("Retrieve Searches called")
    fire = pyrebase.initialize_app(firebaseConfig)
    db = fire.database()
    searches_json = db.child('Searches').get()
    # links = []
    searches = []

    '''
        Return a list of lists of format ['Model', 'Link']
    '''

    for search in searches_json.each():
        new_search = (search.val()['Model'], search.val()['Link'])
        searches.append(new_search)

    # later you could do return links, models
    return searches



def retrieveCars():
    fire = pyrebase.initialize_app(firebaseConfig)
    db = fire.database()
    cars_json = db.child('Cars').get()
    # links = []
    # models = []
    # prices = []
    cars = []
    for car in cars_json.each():
        # print(car.key())
        # print(car.val())
        # print("Link:", search.val()['Link'])
        # print("Model:", search.val()['Model'])
        # print("Price:", search.val()['Price'])
        # links.append(search.val()['Link'])
        # models.append(search.val()['Model'])
        # models.append(search.val()['Price'])
        new_car = (car.val()['Model'], car.val()['Price'], car.val()['Link'])
        cars.append(new_car)

    return cars


def addNewSearch(link, model):
    fire = pyrebase.initialize_app(firebaseConfig)
    db = fire.database()
    search = {
        'Model': model,
        'Link': link
    }
    db.child('Searches').push(search)


def addNewCar(car, link, price):
    fire = pyrebase.initialize_app(firebaseConfig)
    db = fire.database()
    new_car = {
        'Model': car,
        'Price': price,
        'Link': link
    }
    db.child('Cars').push(new_car)


def addNewCars(cars, links, prices):
    fire = pyrebase.initialize_app(firebaseConfig)
    db = fire.database()
    dataJSON = {}

    for i in range(len(cars)):
        uid = str(uuid.uuid1())
        dataJSON[uid] = {
            'Model': cars[i],
            'Price': prices[i],
            'Link': links[i]
        }
    result = db.child('Cars').set(dataJSON)  # throws the fields directly into the thingy
    print("Cars added: ")
    print(result)
    print("length json = ", str(len(str(dataJSON))), ", length result = ", str(len(str(result))))
