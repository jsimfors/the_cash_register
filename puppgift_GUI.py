from tkinter import *
import puppgift

# ----- CREATE WIDGETS --------


class MyWidgets:
    """
    a class to create the GUI, including both the graphics and the actual functions.
    """

    def __init__(self, master):
        self.till = puppgift.Till()
        self.dict_items = puppgift.convert_to_object('in_stock_file.txt')
        frame = Frame(master, bg="yellow")
        master.resizable(width=False, height=False)
        frame.pack()

        # ------- HEADER & TEXTBOX ------------------

        self.header = Label(frame, text="THE BANANA STORE", font=('Times New Roman', 80), bg="#ffff99", fg="black")
        self.header.grid(row=0, column=0, columnspan=5)

        self.underheader = Label(frame, text="", bg="yellow")
        self.underheader.grid(row=1, column=1, columnspan=5)

        self.info_box = Label(frame, text="Banana-codes: 001=Normal Banana   "
                                          "002=Jungle-Banana    003=Dangerous-Banana    004=Poisonous-Banana",
                              bg="#ffff99", fg="black")
        self.info_box.grid(row=3, column=0, columnspan=5, rowspan=2)

        self.underheader2 = Label(frame, text="", bg="yellow")
        self.underheader2.grid(row=6, column=1, columnspan=5)

        self.underheader3 = Label(frame, text="", bg="yellow")
        self.underheader3.grid(row=16, column=1, columnspan=5)

        # ------ LABELS & ENTRIES ---------

        self.buy_label1 = Label(frame, text="What item code?", bg="yellow")
        self.buy_label1.grid(row=7, column=1, sticky=W)

        self.buy_label2 = Label(frame, text="How many?", bg="yellow")
        self.buy_label2.grid(row=8, column=1, sticky=W)

        self.itemcode = Entry(frame, highlightbackground='yellow')
        self.itemcode.grid(row=7, column=2, sticky=W)

        self.amount_entry = Entry(frame, highlightbackground='yellow')
        self.amount_entry.grid(row=8, column=2, sticky=W)

        # ------- TEXT OUTPUTS --------

        self.text_output = Text(frame, bg="#ffff99", width=97, height=1, wrap=WORD)
        self.text_output.grid(row=5, column=0, columnspan=6)

        self.receipt_output = Text(frame, bg="#ffff99", width=55, height=10, wrap=WORD)
        self.receipt_output.grid(row=11, column=0, columnspan=4, rowspan=5)

        # ---- BUTTONS ----------

        self.buyButton = Button(frame, text="Buy", highlightbackground='yellow', command=self.buy_func)
        self.buyButton.grid(row=7, column=3, sticky=W)

        self.returnButton = Button(frame, text="Return", highlightbackground='yellow', command=self.return_func)
        self.returnButton.grid(row=8, column=3, sticky=W)

        self.printReceiptButton = Button(frame, text="Receipt", highlightbackground='yellow',
                                         command=self.print_receipt_func)
        self.printReceiptButton.grid(row=10, column=4)

        self.quitbutton = Button(frame, text="Quit", highlightbackground='yellow', command=frame.quit)
        self.quitbutton.grid(row=11, column=4)

    # --------- METHODS--------------

    def error_handling_code(self, code):
        """
        Checks if the given code is in the right format
        :return: either 'False' or the code itself.
        """

        if code in self.dict_items:
            return code
        else:
            return False

    def buy_func(self):
        """
        Calls the Buy-function from the puppgift-file.
        prints a message to the costumer, ex "You bought 3 Normal-Bananas"
        """

        code = self.itemcode.get()
        number = self.amount_entry.get()
        error_message = "Unable to operate your request, please print a valid "

        if self.error_handling_code(code) is not False:

            if error_handling_int(number) is not False:
                name = self.error_handling_code(code)
                amount = error_handling_int(number)
                name_object = self.dict_items[name]
                to_print = self.till.buy(name_object, amount)
                self.dict_items[code] = puppgift.Item(name_object.item, name_object.price, name_object.amount)
                self.text_output.delete(0.0, END)
                self.text_output.insert(0.0, to_print)

            else:
                self.text_output.delete(0.0, END)
                self.text_output.insert(0.0, error_message + "number")
        else:
            self.text_output.delete(0.0, END)
            self.text_output.insert(0.0, error_message + "code")

    def return_func(self):
        """
        Calls the Return-function from the puppgift-file.
        prints a message to the costumer, ex "You returned 3 Normal-Bananas"
        """

        error_message = "Unable to operate your request, please print a valid "
        code = self.itemcode.get()
        number = self.amount_entry.get()

        if self.error_handling_code(code) is not False:

            if error_handling_int(number) is not False:

                name = self.itemcode.get()
                name_object = self.dict_items[name]
                amount = error_handling_int(number)
                to_print = self.till.return_item(name_object, amount)
                self.dict_items[name] = puppgift.Item(name_object.item, name_object.price, name_object.amount)
                self.text_output.delete(0.0, END)
                self.text_output.insert(0.0, to_print)
            else:
                self.text_output.delete(0.0, END)
                self.text_output.insert(0.0, error_message + "number")

        else:
            self.text_output.delete(0.0, END)
            self.text_output.insert(0.0, error_message + "code")

    def print_receipt_func(self):
        """
        Calls the print_receipt-function from the puppgift-file.
        Prints the receipt in the 'receipt-output'-textbox in the GUI.
        :return:
        """
        to_print = self.till.print_receipt()
        self.receipt_output.delete(0.0, END)
        self.receipt_output.insert(0.0, to_print)
        puppgift.write_to_file(self.dict_items, 'in_stock_file.txt')

# -------- FUNCTIONS -----------


def error_handling_int(number):
    """
    Checks if what's in the "amount" box is an integer
    (and that it's not 0)
    :return: Either the value itself, or False.
    """

    if str(number) is not "0":
        try:
            return int(number)

        except ValueError:
            return False
    else:
        return False


# -------- TO START THE GUI -----

if __name__ == "__main__":
    root = Tk()
    b = MyWidgets(root)
    root.mainloop()
