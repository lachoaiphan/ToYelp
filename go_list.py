import os
import json
import sqlite3
from pathlib import Path


class goList:

    def __init__(self):
        self.go_list = []

    def data_delete(self, conn):
        command = "DELETE FROM go_list"
        cursor = conn.cursor()

        cursor.execute(command)
        conn.commit()

    def data_load(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM go_list")

        d_list = cursor.fetchall()

        # converting tuples into a dictionaries
        for x in range(0, len(d_list)):
            place = {"id": d_list[x][0], "name": d_list[x][1],
                     "address1": d_list[x][2], "city": d_list[x][3],
                     "state": d_list[x][4], "zip_code": d_list[x][5]}
            self.go_list.append(place)

    def data_store(self, conn):
        places = json.loads(Path("go_list.json").read_text())
        command = "INSERT INTO go_list VALUES(?, ?, ?, ?, ?, ?)"

        self.data_delete(conn)  # delete previous data in table to avoid error
        for place in places:
            conn.execute(command, tuple(place.values()))
        conn.commit()

    def set_list(self, conn):
        if len(self.go_list) <= 0:
            print("\nCannot save an empty list!")
            return

        data = json.dumps(self.go_list)
        Path("go_list.json").write_text(data)

        self.data_store(conn)
        print("List has been saved.")

        if os.path.exists("go_list.json"):
            os.remove("go_list.json")
        else:
            print("This JSON file does not exist")

    def select_elem_list(self, names, addrs):
        choice = input("\nEnter the exact name of the place: ")
        for x in range(0, len(names)):
            if names[x].lower() == choice.lower():
                place = {"id": len(self.go_list) + 1, "name": names[x],
                         "address1": addrs[x]["address1"], "city": addrs[x]["city"],
                         "state": addrs[x]["state"],
                         "zip_code": addrs[x]["zip_code"]}
                self.go_list.append(place)
                print("Place has been added.")
                break
        else:
            print("Invalid choice!")

    def clear_list(self, conn):
        warning = input("""WARNING! This will result in your current list
            being cleared! Are you sure? (Y/N): """)
        while True:
            if warning.lower() == 'y':
                self.data_delete(conn)
                self.go_list.clear()
                print("List deleted.")
                break
            elif warning.lower() == 'n':
                break
            else:
                warning = input("Please choose a valid option (Y/N): ")

    def print_to_go_list(self):
        print("%-64s %s" % ("Location:", "Address:"))
        for x in range(0, len(self.go_list)):
            print("%-64s %-1s, %-1s, %-1s %s"
                  % (self.go_list[x]["name"],
                     self.go_list[x]["address1"], self.go_list[x]["city"],
                     self.go_list[x]["state"], self.go_list[x]["zip_code"]))
