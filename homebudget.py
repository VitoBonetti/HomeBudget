import re
import sys
import json
from colorama import Fore
from datetime import datetime

# Logo and Menus
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

main_menu = """
# MAIN MENU #

[1] Insert Supplier
[2] Insert Purchase
[0] Exit

"""

purchase_menu = """

[1] Save Purchase
[2] Back to the Main Menu
[0] Exit

"""

# color setting

error = Fore.RED
menus = Fore.MAGENTA
info = Fore.YELLOW
normal = Fore.CYAN
good = Fore.GREEN
reset = Fore.RESET

# setting filter pattern for supplier names with re

supplier_pattern = re.compile('[@_!#$%^&*()<>?/|}{~:.,;\-+"\']')

# list and dictionary need it for the app to work

main_menu_list = [0, 1, 2]
purchase_menu_list = [0, 1, 2]
suppliers_dict = {}
purchases_dict = {}
supplier_list = []


# functional functions

def nested_dict_value(dictionary_name, list_to_append):
    for k, v in dictionary_name.items():
        if isinstance(v, dict):
            for kk, vv in v.items():
                list_to_append.append(vv)


def check_date_value(date_value):
    try:
        date_purchase = datetime.strptime(date_value, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def check_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def clean_list_and_dict():
    global suppliers_dict, purchases_dict, supplier_list
    suppliers_dict = {}
    purchases_dict = {}
    supplier_list = []

# main functions
def main():
    print(f"{normal}{logo}{reset}")
    menu_main()


def menu_main():
    print(f"{menus}{main_menu}{reset}")
    try:
        choice = int(input(f"{normal}[*] Pick your way: {reset}"))
        if choice in main_menu_list:
            if choice == 0:
                print(f"{chr(27)}[2J")
                print(f"{good}{logo}{reset}")
                print(f"{good}[+] Bye Bye!{reset}")
                sys.exit()
            elif choice == 1:
                print(f"{chr(27)}[2J")
                new_supplier()
            elif choice == 2:
                print(f"{chr(27)}[2J")
                new_purchase()
        else:
            print(f"{chr(27)}[2J")
            print(f"{error}[-] Invalid value{reset}")
            menu_main()
    except ValueError:
        print(f"{chr(27)}[2J")
        print(f"{error}[-] Invalid value. Only numbers allowed.{reset}")
        menu_main()


def new_supplier():
    global suppliers_dict, supplier_list
    print(f"{info}[0] Main Menu{reset}")
    name_supplier = input(f"{normal}[*] Insert supplier name :{reset}")
    if (supplier_pattern.search(name_supplier) is not None) or (name_supplier == ""):
        print(f"{chr(27)}[2J")
        print(f"{error}[-] Invalid value. Special characters are not allowed.{reset}")
        new_supplier()
    else:
        print(f"{chr(27)}[2J")
        # we check if there is already a json file for the suppliers
        try:
            supplier_names = open("suppliers.json", "r")
            suppliers_dict = json.load(supplier_names)
        except FileNotFoundError:
            pass

        # extract the supplier names

        nested_dict_value(suppliers_dict, supplier_list)

        # check if the name of the new supplier is already register

        if name_supplier in supplier_list:
            print(f"{chr(27)}[2J")
            print(f"{error}[-] Supplier already exist{reset}")
            clean_list_and_dict()
            new_supplier()
        else:
            # check if the user want to come back at the main menu
            if name_supplier == "0":
                print(f"{chr(27)}[2J")
                menu_main()
            else:
                # assign an id to the supplier
                try:
                    supplier_id = int(list(suppliers_dict.keys())[-1])+1
                except (IndexError, UnboundLocalError):
                    supplier_id = 0
                # register the supplier in the dictionary and then save it on json file
                suppliers_dict[supplier_id] = {}
                suppliers_dict[supplier_id]['Name'] = name_supplier
                with open("suppliers.json", "w") as json_supplier:
                    json.dump(suppliers_dict, json_supplier, indent=4, separators=(",", ":"))
                print(f"{chr(27)}[2J")
                print(f"{good}[+] Supplier added successfully.{reset}")
                clean_list_and_dict()
                menu_main()


def new_purchase():
    global purchases_dict, supplier_list, suppliers_dict
    print(f"{chr(27)}[2J")
    while True:
        get_date = input(f"{normal}[*] Purchase date{reset}{info} (dd-mm-yyy){reset}{normal}:{reset} ")
        if check_date_value(get_date):
            purchase_date = datetime.strptime(get_date, "%d-%m-%Y").strftime("%d-%m-%Y")
            print(f"{chr(27)}[2J")
            break
        else:
            print(f"{chr(27)}[2J")
            print(f"{error}[-] Not a valid Format. The date must be in dd-mm-yyyy format.{reset}")
    while True:
        try:
            suppliers_info = open("suppliers.json", "r")
            suppliers_dict = json.load(suppliers_info)
            for k, v in suppliers_dict.items():
                if isinstance(v, dict):
                    for kk, vv in v.items():
                        supplier_list.append(vv)

            print(f"{menus}# SUPPLIERS LIST #{menus}")
            item_supplier = 1
            for item in supplier_list:
                print(f"{menus}[{item_supplier}] {item}{reset}")
                item_supplier += 1
            try:
                get_supplier = int(input(f"{normal}[*] Pick the supplier: {reset}"))
                if 1<= get_supplier <= len(supplier_list):
                    supplier_list_index = get_supplier - 1
                    purchase_supplier = supplier_list[supplier_list_index]
                    clean_list_and_dict()
                    print(f"{chr(27)}[2J")
                    break
                else:
                    print(f"{chr(27)}[2J")
                    print(f"{error}[-] Supplier not in the list{reset}")
                    clean_list_and_dict()
                    continue
            except ValueError:
                print(f"{chr(27)}[2J")
                print(f"{error}[-] Only number allowed.{reset}")
                clean_list_and_dict()
                continue
        except FileNotFoundError:
            print(f"{chr(27)}[2J")
            print(f"{error}[-] There is no data for the supplier{reset}")

    while True:
        get_btw9 = input(f"{normal}Insert BTW 9%: € {reset}")
        if check_float(get_btw9):
            purchase_btw9 = float(get_btw9)
            print(f"{chr(27)}[2J")
            break
        else:
            print(f"{chr(27)}[2J")
            print(f"{error}[-] Not a valid Format. Only number o decimal number allowed{reset}")
            continue

    while True:
        get_btw21 = input(f"{normal}Insert BTW 21%: € {reset}")
        if check_float(get_btw21):
            purchase_btw21 = float(get_btw21)
            print(f"{chr(27)}[2J")
            break
        else:
            print(f"{chr(27)}[2J")
            print(f"{error}[-] Not a valid Format. Only number o decimal number allowed{reset}")
            continue

    while True:
        get_statigeld = input(f"{normal}Insert StatiGeld: € {reset}")
        if check_float(get_statigeld):
            purchase_statigeld = float(get_statigeld)
            print(f"{chr(27)}[2J")
            break
        else:
            print(f"{chr(27)}[2J")
            print(f"{error}[-] Not a valid Format. Only number o decimal number allowed{reset}")
            continue

    while True:
        get_discount = input(f"{normal}Insert Discount: € {reset}")
        if check_float(get_discount):
            purchase_discount = float(get_discount)
            print(f"{chr(27)}[2J")
            break
        else:
            print(f"{chr(27)}[2J")
            print(f"{error}[-] Not a valid Format. Only number o decimal number allowed{reset}")
            continue

    while True:
        get_total = input(f"{normal}Insert Total : € {reset}")
        if check_float(get_total):
            purchase_total = float(get_total)
            print(f"{chr(27)}[2J")
            break
        else:
            print(f"{chr(27)}[2J")
            print(f"{error}[-] Not a valid Format. Only number o decimal number allowed{reset}")
            continue

    print(f"{menus}# SUMMARY OF DATA ENTERED #{reset}")
    print(f"{menus}[*] Purchase on: {reset}{normal}{purchase_date}{reset}")
    print(f"{menus}[*] Supplier: {reset}{normal}{purchase_supplier}{reset}")
    print(f"{menus}[*] Expense BTW 9%: {reset}{normal}{purchase_btw9} €{reset}")
    print(f"{menus}[*] Purchase on: {reset}{normal}{purchase_btw21} €{reset}")
    print(f"{menus}[*] Purchase on: {reset}{normal}{purchase_statigeld} €{reset}")
    print(f"{menus}[*] Purchase on: {reset}{normal}{purchase_discount} €{reset}")
    print(f"{menus}[*] Purchase on: {reset}{normal}{purchase_total} €{reset}")
    while True:
        try:
            print(f"{menus}{purchase_menu}{reset}")
            choice = int(input(f"{normal}Pick your way: {reset}"))
            if choice in purchase_menu_list:
                if choice == 0:
                    print(f"{chr(27)}[2J")
                    print(f"{good}{logo}{reset}")
                    print(f"{good}[+] Bye Bye!{reset}")
                    sys.exit()
                elif choice == 2:
                    print(f"{chr(27)}[2J")
                    clean_list_and_dict()
                    menu_main()
                elif choice == 1:
                    try:
                        purchases_info = open("purchases.json", "r")
                        purchases_dict = json.load(purchases_info)
                    except FileNotFoundError:
                        pass
                    try:
                        purchase_id = int(list(purchases_dict.keys())[-1])+1
                    except (IndexError, UnboundLocalError):
                        purchase_id = 0
                    purchases_dict[purchase_id] = {}
                    purchases_dict[purchase_id]["Date"] = purchase_date
                    purchases_dict[purchase_id]["Supplier"] = purchase_supplier
                    purchases_dict[purchase_id]["Btw9"] = purchase_btw9
                    purchases_dict[purchase_id]["Btw21"] = purchase_btw21
                    purchases_dict[purchase_id]["Statigeld"] = purchase_statigeld
                    purchases_dict[purchase_id]["Discount"] = purchase_discount
                    purchases_dict[purchase_id]["Total"] = purchase_total
                    with open("purchases.json", "w") as json_purchase:
                        json.dump(purchases_dict, json_purchase, indent=4, separators=(",", ":"))
                    break
            else:
                print(f"{chr(27)}[2J")
                print(f"{error}[-] Invalid value{reset}")
                continue
        except ValueError:
            print(f"{chr(27)}[2J")
            print(f"{error}[-] Invalid value{reset}")
            continue

    print(f"{chr(27)}[2J")
    print(f"{good}[+] Purchase added successfully.{reset}")
    clean_list_and_dict()
    menu_main()

main()
