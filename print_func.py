def print_menu():
    options = """
        1. Add to Your To-Go List
        2. Print out Your List
        3. Save Current List
        4. Delete Current List
        5. Quit
    """
    print(options)


def addr_concat(addr1, addr2, addr3):
    addr = ""
    if len(addr1) > 0:
        addr = addr + addr1
    if len(addr2) > 0:
        addr = addr + addr2
    if len(addr3) > 0:
        addr = addr + addr3

    return addr


def print_list(names, addrs):
    # print lists from yelp business endpoints
    print("%-64s %s" % ("\nLocation:", "Address:"))
    for x in range(0, len(names)):
        address = addr_concat(addrs[x]["address1"],
                              str(addrs[x]["address2"]),
                              str(addrs[x]["address3"]))
        print("%-64s %-1s, %-1s, %-1s %s"
              % (names[x],
                 address, addrs[x]["city"],
                 addrs[x]["state"], addrs[x]["zip_code"]))
