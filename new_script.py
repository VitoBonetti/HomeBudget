import re
import sys
from colorama import Fore
import json
from datetime import datetime

logo = """
┏┓╋┏┓╋╋╋╋╋╋╋╋╋┏━━┓╋╋╋╋╋┏┓╋╋╋╋╋┏┓
┃┃╋┃┃╋╋╋╋╋╋╋╋╋┃┏┓┃╋╋╋╋╋┃┃╋╋╋╋┏┛┗┓
┃┗━┛┣━━┳┓┏┳━━┓┃┗┛┗┳┓┏┳━┛┣━━┳━┻┓┏┛
┃┏━┓┃┏┓┃┗┛┃┃━┫┃┏━┓┃┃┃┃┏┓┃┏┓┃┃━┫┃
┃┃╋┃┃┗┛┃┃┃┃┃━┫┃┗━┛┃┗┛┃┗┛┃┗┛┃┃━┫┗┓
┗┛╋┗┻━━┻┻┻┻━━┛┗━━━┻━━┻━━┻━┓┣━━┻━┛
╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋┏━┛┃
╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋╋┗━━┛v0.1
"""
options_menu = """
[1] Insert Supplier
[2] Insert Purchase
[3] Exit
"""

suppliers = {}
purchases = {}
temp_suppliers_list = []
options_list = [1,2,3]

# suppliers_starting_id = 1
purchases_starting_id = 1

supplier_string_pattern = re.compile('[@_!#$%^&*()<>?/|}{~:.,;\-+"\']')

error = Fore.RED
info = Fore.MAGENTA
normal = Fore.CYAN
good = Fore.GREEN
reset = Fore.RESET

def check_float(number):
    if number == "":
        number = 0
    try:
        float(number)
        return True
    except ValueError:
        return False


def insert_purchase_btw9():
    get_purchase_9 = input(f"{normal}Insert BTW 9%{reset}: ")
    if check_float(get_purchase_9):
        return get_purchase_9
    else:
        return False
    # try:
    #     float(get_purchase_9)
    #     return get_purchase_9
    # except ValueError:
    #     print(f"{error}Not a valid Format. Only number o decimal number allowed{reset}")
    #     insert_purchase_btw9()


def insert_purchase_btw21():
    get_purchase_21 = input(f"{normal}Insert BTW 21%{reset}: ")
    if check_float(get_purchase_21):
        return float(get_purchase_21)
    else:
        print(f"{error}Not a valid Format. Only number o decimal number allowed{reset}")
        insert_purchase_btw21()


def insert_purchase_statigeld():
    get_purchase_statigeld = input(f"{normal}Insert Statigeld{reset}: ")
    if check_float(get_purchase_statigeld):
        return float(get_purchase_statigeld)
    else:
        print(f"{error}Not a valid Format. Only number o decimal number allowed{reset}")
        insert_purchase_statigeld()


def insert_purchase_discount():
    get_purchase_discount = input(f"{normal}Insert Discount{reset}: ")
    if check_float(get_purchase_discount):
        return float(get_purchase_discount)
    else:
        print(f"{error}Not a valid Format. Only number o decimal number allowed{reset}")
        insert_purchase_discount()


def insert_purchase_total():
    get_total = input(f"{normal}Insert Total Amount{reset}: ")
    if check_float(get_total):
        return float(get_total)
    else:
        print(f"{error}Not a valid Format. Only number o decimal number allowed{reset}")
        insert_purchase_total()

def insert_purchase_date():
    get_purchase_date = input(f"{normal}Insert the date{reset}{info} (Format dd-mm-yyyy): {reset}")
    try:
        purchase_date = (datetime.strptime(get_purchase_date, "%d-%m-%Y").strftime("%d-%m-%Y"))
        return purchase_date
    except ValueError:
        print(f"{error}Not a valid Format. The date must be in dd-mm-yyyy format.{reset}")
        insert_purchase_date()

def insert_purchase_supplier():
    global temp_suppliers_list
    create_supplier_list()
    print(f"{info}Suppliers List {reset}")
    item_number = 1
    for item in temp_suppliers_list:
        print(f"{normal}[{item_number}] {item}{reset}")
        item_number += 1
    try:
        get_supplier = int(input(f"{normal}Pick the supplier: {reset}"))
        if 1 <= get_supplier <= len(temp_suppliers_list):
            list_index = get_supplier - 1
            supplier_purchase = temp_suppliers_list[list_index]
            temp_suppliers_list = []
            return supplier_purchase
        else:
            print(f"{error}[-] Supplier not in the List. {reset}")
            insert_purchase_supplier()
    except ValueError:
        print(f"{error}Only number allowed.{reset}")
        insert_purchase_supplier()

def insert_purchase():
    purchase_date = insert_purchase_date()
    purchase_supplier = insert_purchase_supplier()
    purchase_9 = insert_purchase_btw9()
    purchase_21 = insert_purchase_btw21()
    purchase_statigeld = insert_purchase_statigeld()
    purchase_discount = insert_purchase_discount()
    purchase_total = insert_purchase_total()

    print(purchase_date)
    print(purchase_supplier)
    print(purchase_9)
    print(purchase_21)
    print(purchase_statigeld)
    print(purchase_discount)
    print(purchase_total)


def insert_supplier():
    global suppliers
    print(f"{info} Use 0 for go back to the main Page.")
    new_supplier = input(f"{normal}[*] Insert the name of the new supplier: {reset}")
    if supplier_string_pattern.search(new_supplier) is not None or new_supplier == "":
        print(f"{error}[-] The name can't contain special characters or be empty.{reset}")
        insert_supplier()
    else:
        try:
            suppliers_data = open("supplier.json", "r")
            suppliers = json.load(suppliers_data)
        except FileNotFoundError:
            pass

        for k, v in suppliers.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    temp_suppliers_list.append(vv)

        if new_supplier in temp_suppliers_list:
            print(f"{error}[-] Supplier already in the list{reset}")
            insert_supplier()
        else:
            if new_supplier == "0":
                option_menu()
            try:
                suppliers_starting_id = int(list(suppliers.keys())[-1]) + 1
            except (IndexError, UnboundLocalError):
                suppliers_starting_id = 1
            suppliers[suppliers_starting_id] = {}
            suppliers[suppliers_starting_id]["name"] = new_supplier
            with open("supplier.json", "w") as json_file:
                json.dump(suppliers, json_file, indent=4, separators=(",", ":"))
                print(f"{good}[+] File successfully Update.{reset}")
                insert_supplier()


def create_supplier_list():
    global temp_suppliers_list, suppliers
    try:
        suppliers_data = open("supplier.json", "r")  # to delete
        suppliers = json.load(suppliers_data)  # to delete
        for k, v in suppliers.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    temp_suppliers_list.append(vv)
        # print(temp_suppliers_list)
        # option_menu()
    except FileNotFoundError:
        print(f"{error}[-] There is no data for the supplier. The program will be terminated.")
        sys.exit()

def option_menu():
    print(f"{normal}- Options Menu -{reset}")
    print(f"{normal}{options_menu}{reset}")
    try:
        choice = int(input(f"{info}[*] Make your choice: {reset}"))
        if not choice in options_list:
            print(f"{error}[-] Unknown choice. {reset}")
            option_menu()
        else:
            if choice == 1:
                insert_supplier()
            elif choice == 2:
                create_supplier_list()
            elif choice == 3:
                print(f"{good}[+] Bye Bye!{reset}")
                sys.exit()
    except ValueError:
        print(f"{error}[-] Can be only number. No empty value allowed. {reset}")
        option_menu()

def main():
    print(f"{normal}{logo}{reset}")
    option_menu()

insert_purchase()
