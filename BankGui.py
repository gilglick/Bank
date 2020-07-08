# HW3 JONATHAN KARTA
from tkinter import *
import BankCompany
from tkinter import ttk
from tkinter import messagebox


class Application(object):
    def __init__(self, master, bank_comapany, file_name):
        self.bankCompany = bank_comapany
        self.top = self.bottom = self.bottom_right = self.bottom_left = self.bottom_lower = None
        self.current_customer = None
        self.list_index = 0
        self.file_name = file_name
        self.master = master
        self.master.geometry('700x400+350+300')
        self.master.title("Jon's bank")
        self.master.resizable(True, True)

        # Hold the top main frame and the bottom main frame
        self.create_main_frame()

        # Bank icon
        self.bank_icon = PhotoImage(file='icons/bank.png')
        self.bank_button = Label(self.top, image=self.bank_icon, compound=CENTER, bg="white")
        self.bank_button.pack()

        # Withdraw icon and button
        self.withdraw_icon = PhotoImage(file='icons/withdraw.png')
        self.withdraw_button = Button(self.bottom_lower, text="Withdraw", image=self.withdraw_icon, compound=LEFT
                                      , command=self.withdraw)
        self.withdraw_button.pack(side=LEFT, padx=10)

        # Deposit icon and button
        self.deposit_icon = PhotoImage(file='icons/deposit.png')
        self.deposit_button = Button(self.bottom_lower, text="Deposit", image=self.deposit_icon, compound=LEFT
                                     , command=self.deposit)
        self.deposit_button.pack(side=LEFT, padx=10)

        self.entry = Entry(self.bottom_lower, textvariable=1, font="ariel 15", width=10)
        self.entry.pack(side=LEFT, pady=5)

        # Transfer money icon and button
        self.transfer_icon = PhotoImage(file='icons/transfer.png')
        self.transfer_button = Button(self.bottom_lower, text="Transfer", image=self.transfer_icon, compound=LEFT
                                      , command=self.transfer_money_win)
        self.transfer_button.pack(side=LEFT, padx=10)

        # Frame for the scrollbar
        self.bottom_left_frame = Frame(self.bottom_left, width=50, height=50, bg="brown")
        self.bottom_left_frame.pack(side=LEFT)
        self.listbox = Listbox(self.bottom_left_frame, width=40, height=50, bg="white", font="Helvetica 9 italic")
        self.scrollbar = Scrollbar(self.bottom_left_frame, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)
        self.listbox.pack()

        # Frame of right pane
        self.customer_info = LabelFrame(self.bottom_right, text=" Customer information ", height=800,
                                        bg="#9bc9ff",
                                        font="Times 12 bold italic")
        self.customer_info.pack(fill=BOTH)

        self.customer_name = Label(self.bottom_right, text="Name :", bg="#9bc9ff", font="Times 12 bold italic")
        self.customer_name.place(x=10, y=30)

        self.customer_name = Label(self.bottom_right, text="Account :", bg="#9bc9ff", font="Times 12 bold italic")
        self.customer_name.place(x=10, y=70)

        self.customer_name = Label(self.bottom_right, text="Balance :", bg="#9bc9ff", font="Times 12 bold italic")
        self.customer_name.place(x=10, y=110)

        self.customer_name = Label(self.bottom_right, text="Credit :", bg="#9bc9ff", font="Times 12 bold italic")
        self.customer_name.place(x=10, y=150)

        self.str_name = StringVar()
        self.extract_name = Label(self.bottom_right, font="Times 12 italic", bg="#9bc9ff", textvariable=self.str_name)
        self.extract_name.place(x=100, y=30)

        self.str_account = StringVar()
        self.extract_account = Label(self.bottom_right, font="Times 12 italic", bg="#9bc9ff",
                                     textvariable=self.str_account)
        self.extract_account.place(x=100, y=70)

        self.str_balance = StringVar()
        self.extract_balance = Label(self.bottom_right, font="Times 12 italic", bg="#9bc9ff",
                                     textvariable=self.str_balance)
        self.extract_balance.place(x=100, y=110)

        self.str_credit = StringVar()
        self.extract_credit = Label(self.bottom_right, font="Times 12  italic", bg="#9bc9ff",
                                    textvariable=self.str_credit)
        self.extract_credit.place(x=100, y=150)

        # Transfer money pane
        self.entry_amount = self.account_number = self.box = None

        # Functionality
        self.read_customer_from_file()
        self.create_customer_listbox()
        self.listbox.bind('<<ListboxSelect>>', self.update_customer)
        self.listbox.select_set(0)  # This only sets focus on the first item.
        self.update_customer(self)

    def create_main_frame(self):
        self.top = Frame(self.master, bg="white", relief=SUNKEN, borderwidth=2)
        self.bottom = Frame(self.master, relief=SUNKEN, borderwidth=2)
        self.bottom_right = Frame(self.bottom, height=800, relief=SUNKEN, borderwidth=2)
        self.bottom_left = Frame(self.bottom, relief=SUNKEN, borderwidth=2)
        self.bottom_lower = Frame(self.bottom, relief=SUNKEN, borderwidth=2)
        self.top.pack(side=TOP, fill=BOTH)
        self.bottom.pack(side=BOTTOM, fill=BOTH)
        self.bottom_lower.pack(side=BOTTOM, fill=BOTH)
        self.bottom_left.pack(side=LEFT)
        self.bottom_right.pack(fill=BOTH)

    def withdraw(self):
        if self.entry.get().isdigit():
            self.current_customer = self.bankCompany.customers[self.get_customer_index()]
            if self.current_customer.withdraw(int(self.entry.get())):
                self.update_customer(self)

        else:
            messagebox.showerror("Error", "You insert invalid argument to the fields.")
            return

    def deposit(self):
        if self.entry.get().isdigit():
            self.current_customer = self.bankCompany.customers[self.get_customer_index()]
            self.current_customer.deposit(int(self.entry.get()))
            self.update_customer(self)
        else:
            messagebox.showerror("Error", "You insert invalid argument to the fields.")

    def update_customer(self, event):
        try:
            self.current_customer = self.bankCompany.customers[self.get_customer_index()]
            self.str_name.set(self.current_customer.customer_name)
            self.str_account.set(self.current_customer.account_number)
            self.str_balance.set(self.current_customer.balance)
            self.str_credit.set(self.current_customer.credit_limit)
        except:
            return

    def read_customer_from_file(self):
        with open(self.file_name, "r") as f:
            for customer in f:
                obj = customer.split(",")
                name, account_number, amount, credit = obj[0], obj[1], obj[2], obj[3]
                self.bankCompany.add_customer(BankCompany.Account(name, int(account_number), int(amount), int(credit)))

    def create_customer_listbox(self):
        for index, customer in enumerate(self.bankCompany.customers):
            self.listbox.insert(index, customer.customer_name)

    def get_customer_index(self):
        try:
            self.list_index = int(self.listbox.curselection()[0])
            return self.list_index
        except:
            return self.list_index

    def transfer_to_account(self):
        try:
            if self.entry_amount.get().isdigit():
                customer = self.bankCompany.customers[self.box.current()]
                if self.current_customer.account_number != customer.account_number:
                    if self.current_customer.deposit_to_account(customer, int(self.entry_amount.get())):
                        self.update_customer(self)
                        messagebox.showinfo("Transaction message",
                                            f"Transaction from account {self.current_customer.account_number} "
                                            f"to account {customer.account_number} executed successfully ")
                else:
                    messagebox.showerror("Error", "Cannot make transaction to the same account")
            else:
                messagebox.showerror("Error", "You insert invalid argument to the fields.")
        except TclError:
            return

    def transfer_money_win(self):
        secondary_win = Toplevel()
        secondary_win.geometry("300x300+950+250")

        top_frame = Frame(secondary_win, width=300, height=80, bg="#9bc9ff", borderwidth=4, relief=RIDGE)
        bottom_frame = Frame(secondary_win, width=300, height=236, borderwidth=4, relief=RIDGE)
        top_frame.pack()
        bottom_frame.pack()

        header = Label(top_frame, text="Money Transfer", bg="#9bc9ff", font="Times 25 bold italic")
        header.place(x=35, y=20)

        amount = Label(bottom_frame, text="Amount:", font="Times 12 bold italic")
        amount.grid(row=0, column=0, padx=20, pady=20)
        self.entry_amount = Entry(bottom_frame)
        self.entry_amount.grid(row=0, column=1, padx=20, pady=20)
        transfer_label = Label(bottom_frame, text="Transfer to:", font="Times 12 bold italic")
        transfer_label.grid(row=1, column=0, padx=20, pady=20)
        self.box = ttk.Combobox(bottom_frame, values=[n.account_number for n in self.bankCompany.customers])
        self.box.current(0)
        self.box.grid(row=1, column=1)

        confirm_button = Button(bottom_frame, text="Confirm Transaction", command=self.transfer_to_account,
                                font="Times 10 bold")
        confirm_button.grid(row=2, column=0, pady=30)


if __name__ == '__main__':
    bankCompany = BankCompany.Bank("Jon's bank")
    root = Tk()
    app = Application(root, bankCompany, "Customers")
    root.mainloop()
