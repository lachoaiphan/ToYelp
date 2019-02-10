import config
import requests
import sqlite3
import print_func
from sqlite3 import Error
from go_list import goList


def create_connection():
    # creating a connection to the database
    try:
        conn = sqlite3.connect("db.sqlite3")
        return conn
    except Error as e:
        print(e)

    return None


def add_to_go_list(go_list):
    term = input("Enter the term you want (Food/Barber/etc): ")
    location = input("Enter the location you want: ")

    url = "https://api.yelp.com/v3/businesses/search"

    headers = {
        "Authorization": "Bearer " + config.api_key
    }

    params = {
        "term": term,
        "location": location
    }

    # getting data from Yelp Business Endpoint
    response = requests.get(url, headers=headers, params=params)
    businesses = response.json()["businesses"]

    names = [business["name"] for business in businesses]
    addrs = [business["location"] for business in businesses]

    # if no data was retrieved based on inputs
    if not names or not addrs:
        print("No names associated with the inputs you have given.")
    else:
        print_func.print_list(names, addrs)
        while True:
            choice = input(
                "Would you like to add a place to your list? (Y/N): ")
            if choice.lower() == "y":
                go_list.select_elem_list(names, addrs)
            elif choice.lower() == 'n':
                break
            else:
                print("Invalid choice! Try again!")


def main():
    go_list = goList()  # created a class to handle a list with REST API
    conn = create_connection()  # establishes connection to database

    # if connection cannot be established
    if type(conn) == None:
        return None

    go_list.data_load(conn)  # loads previous data from last session

    print("\nWelcome to ToYelp!")
    while True:
        print_func.print_menu()

        choice = input("Select a valid option: ")
        if choice == "1":
            add_to_go_list(go_list)
            # add to go list from yelp business endpoints
        elif choice == "2":
            go_list.print_to_go_list()
            # prints current list that is not saved
        elif choice == '3':
            go_list.set_list(conn)
            # insert current data into table
        elif choice == '4':
            go_list.clear_list(conn)
            # deletes data from table and list
        elif choice == '5':
            break
        else:
            print("\nInvalid choice detected.")


if __name__ == "__main__":
    main()
