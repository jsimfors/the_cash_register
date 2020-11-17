class Item:
    """
    Attributes:
    item: what kind of item, ex banana
    price: the price of the item
    amount: the amount left in stock
    """

    def __init__(self, item, price, amount):
        """
        :param item: what kind of item, ex. banana
        :param price: The price of the item
        :param amount: the amount left in stock
        """
        self.item = item
        self.amount = int(amount)
        self.price = price

    def __str__(self):
        """
            prints the item name of the item, ex. banana
        """
        return self.item

    def decrease_stock(self, units):
        """
            is used to decrease the amount of a certain item.
           This method runs every time we use the 'buy' method from the 'Till' class.
           :param units: The amount of, ex. bananas, we want to buy/reduce from stock.
           :return: The amount left in stock, or False (if there's not enough in Stock)
        """

        if self.amount >= units:
            self.amount -= units
            return self.amount
        else:
            return False

    def raise_stock(self, units):
        """
        Used to add items to stock, runs every time we use the "return item" method in the 'Till' class.
        :param units: amount of items we want to add in stock.
        :return: The amount
        """
        self.amount += units
        return self.amount


class Till:
    """
    Keeps track of the current transaction.
    """

    def __init__(self):
        """
        current_transaction = A receipt, key = name of the item.
        price_and_amount = A list of the price and amount of the item.
        used as the value in the current_transactions dictionary.
        """
        self.current_transaction = {}
        self.price_and_amount = []

    def print_receipt(self):
        """
        Adds the current_transaction dictionary to the receipt.
        Deletes an item if the customer returns all the purchased units.
        Is used when the customer press # = Exit
        :return: A receipt, with all information including total price.
        """
        all_total = 0
        str_current_transactions = ""

        for i in self.current_transaction:
            total = self.current_transaction[i][2]
            all_total += total
            to_add = "{0:18}{1:0}      {2:8}{3:0}\n".format(i, self.current_transaction[i][0],
                                                            self.current_transaction[i][1],
                                                            self.current_transaction[i][2])
            str_current_transactions += str(to_add)

        return '----------------- RECEIPT -----------------\nItem             Amount  A-price  Total\n{}\n' \
               '                                 total: {}'.format(str_current_transactions, round(all_total, 2))

    def buy(self, item, units):
        """
        Used to add items to receipt, this method calls the 'decrease_stock' method
        If decrease_stock returns false, it'll print 'Not enough in stock".
        :param item: name of the item, ex Banana.
        :param units: Amount of items the customer buys
        :returns: information about what the customer bought/that it's not in stock.
        """

        if Item.decrease_stock(item, units) is not False:

            price = item.price
            value_list = []
            str_item = str(item)

            if str_item in self.current_transaction:
                self.current_transaction[str_item][0] += units
                self.current_transaction[str_item][2] = \
                    round(int(self.current_transaction[str_item][0]) * float(self.current_transaction[str_item][1]), 2)
                return "You bought {} {}s".format(units, str_item)

            else:
                cost = round((int(units) * float(price)), 2)
                value_list.append(units)
                value_list.append(price)
                value_list.append(cost)
                self.current_transaction[str_item] = value_list
                return "You bought {} {}s".format(units, str_item)

        else:
            return "Not enough {}s in stock".format(item)

    def return_item(self, item, units):
        """
        Used to remove items from receipt. Calls the raise_stock in the Item class.
        :param item: name of the item, ex Banana.
        :param units: Amount of items the customer returns
        :return: information about what the customer returned
        """
        str_item = str(item)

        if str_item in self.current_transaction:

            if self.current_transaction[str_item][0] >= units:
                self.current_transaction[str_item][0] -= units
                self.current_transaction[str_item][2] = \
                    round(int(self.current_transaction[str_item][0]) * float(self.current_transaction[str_item][1]), 2)

                Item.raise_stock(item, units)

                if self.current_transaction[str_item][0] == 0:
                    del self.current_transaction[str_item]

                return "You returned {} {}s".format(units, str_item)

            else:
                return "You can't return more bananas than you bought"

        else:
            return "You did not buy any {}s".format(item)


def get_int_input(prompt_string):
    """
    checks if the input is either a # or an integer
    :param prompt_string: the input the customer buys
    :return: An integer or an Error message.
    """
    done = False
    while done is not True:
        string = input(prompt_string)
        if string is not "0":
            try:
                return int(string)

            except ValueError:
                print("Unable to operate your request, please print a valid number.")
                done = False
        else:
            print("0 is not an option")
            done = False


def get_int_menu_input(choice_string):
    """
    needs this error-handling-function, since the menu has 1, 2, OR the '#' as an option.
    But the rest of the program just want's to check if it's an integer.
    :param choice_string: the input, from the customer
    :return: An integer, the string '#' or an Error message.
    """
    done = False
    while done is not True:
        choice = input(choice_string)
        if choice == '#':
            return '#'
        else:
                try:
                    return int(choice)

                except ValueError:
                    print("Unable to operate your request, please print a valid option.")
                    done = False


def get_item_code(code, all_items):
    """
    Checks if the input from the customer corresponds with an item in stock
    :param code: the item code, ex 001, 002...
    :param all_items dictionary with all the items
    :return: The item code or Error message.
    """

    done = not True

    while done is not True:
        if code in all_items:
            return code
        else:
            print("Unable to operate your request, please print a valid code.")
            done = False
            code = input()


def read_data_from_file(in_stock_file):

    """
    Used to get information about the items in Stock.
    :param in_stock_file: a file with all the information
    :return: all_items, a dictionary with all data on it
    """

    all_items = {}

    with open(in_stock_file) as f:
        for line in f:
            all_as_list = line.split()
            all_items[all_as_list[0]] = all_as_list[1:4]
    return all_items


def convert_to_object(textfile):
    """
    Converts the dictionary to an object for the Till class.
    :param textfile: a file with all the information
    :return: Objects for the Till class.
    """
    all_items_obj = read_data_from_file(textfile)
    for key in all_items_obj:
        all_as_list = all_items_obj[key]
        all_items_obj[key] = Item(all_as_list[0], all_as_list[1], all_as_list[2])
    return all_items_obj


def write_to_file(my_obj, in_stock_file):
    """
    When the customer is done shopping, this function takes the new information about what's left in stock,
    and updates the textfile.
    :param my_obj: the object from the Till class.
    :param in_stock_file: A textfile, where we rite all the information.
    :return: nothing
    """
    f = open(in_stock_file, "w")
    for i in my_obj:
        to_write = str(i) + " " + str(my_obj[i].item) + " " + str(my_obj[i].price) + " " + str(my_obj[i].amount)
        f.writelines(to_write + '\n')


def menu(till, dict_items):
    """
    Used to display a meny for the user. With the options:
    1 - Shopping
    2 - Return item
    # - Exit
    :return: nothing
    """
    print("""
-------------------------------
Hello Banana-Customer!
What would you like to do?
1 - Shopping
2 - Return item
# - Exit""")
    execute(menu_choice(), dict_items, till)


def menu_choice():
    """
    Used to get input on what the customer wants to do
    :return: choice = an int, the chosen menu option
    """
    return get_int_menu_input('Answer: ')


def execute(choice, all_items, till):
    """
    used to execute the option that the user chose, calls a specific method from the Till class
    :param choice: and int corresponding to the chosen option (from menu_choice() )
    :param all_items: the objects for the Till class ?? eller?
    :param till: object to the till class.
    :return: nothing
    """

    while choice != '#':
        if choice == 1:
            code = input("""What do you want to buy?
Normal Banana=001
Jungle Banana=002
Dangerous-Banana=003
Poisonous-Banana=004""")
            name = get_item_code(code, all_items)
            name_object = all_items[name]
            amount = get_int_input("How many? ")
            till.buy(name_object, amount)
            all_items[name] = Item(name_object.item, name_object.price, name_object.amount)

        elif choice == 2:
            code = input("What would you like to return?")
            name = get_item_code(code, all_items)
            name_object = all_items[name]
            amount = get_int_input("How many? ")
            till.return_item(name_object, amount)
            all_items[name] = Item(name_object.item, name_object.price, name_object.amount)

        else:
            print("There's obviously only 2 options...")

        menu(till, all_items)

    else:
        print(till.print_receipt())
        write_to_file(all_items, 'in_stock_file.txt')
        exit()


def main():
    """
    To start program.
    """
    my_till = Till()
    my_items = convert_to_object('in_stock_file.txt')
    menu(my_till, my_items)


# To start program without the GUI:
# main()
