import sqlite3
import re
import os
import sys
import datetime
from colorama import Fore
from os import system, name

list_choise = [1,2,3]
supplier_string_pattern = re.compile('[@_!#$%^&*()<>?/|}{~:.,;\-+"\']')
title = "## Home Budget v0.1 ##"
menu = """
[*] Make your choice:
[1] Insert Supplier
[2] Insert Purchase
[3] Exit
"""


def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def main():
    create_db()
    print(title)
    choices_menu()

def choices_menu():
    print(menu)
    try:
        choice = int(input("[*] Your choice: "))
        if choice in list_choise:
            if choice == 1:
                insert_supplier()
            elif choice == 2:
                print(f"{Fore.GREEN}[+] Insert Purchase{Fore.RESET}")
                choices_menu()
            elif choice == 3:
                print(f"{Fore.CYAN}[+] Ok, bye bye!{Fore.RESET}")
                sys.exit()
        else:
            print(f"{Fore.MAGENTA}[-] Nope, again{Fore.RESET}")
            # clear_screen()
            choices_menu()
    except ValueError as e:
        print(f"{Fore.RED}[-] {e}{Fore.RESET}")
        # clear_screen()
        choices_menu()

def open_db():
    conn = sqlite3.connect("test.db")
    return conn

def create_db():
    conn = open_db()
    cur = conn.cursor()
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS supplier (name TEXT NOT NULL UNIQUE)")
        cur.execute("""CREATE TABLE IF NOT EXISTS  purchases (
                    purchased_on TEXT NOT NULL,
                    supplier TEXT NOT NULL,
                    amout_9 REAL,
                    amount_21 REAL,
                    statigeld REAL,
                    discount REAL,
                    amount_tot REAL NOT NULL
                    )""")
        conn.commit()
        conn.close()
        return conn, cur
    except sqlite3.OperationalError as e:
        conn.close()
        print(f"Supplier: {e}")
        return conn, cur

def insert_supplier():
    conn = open_db()
    cur = conn.cursor()
    new_supplier = input(f"{Fore.GREEN}Insert new supplier name: {Fore.RESET}")
    if (supplier_string_pattern.search(new_supplier) is not None) or new_supplier == "":
        print(f"{Fore.MAGENTA}The name can't contain special character or be an empty string.")
        insert_supplier()
    else:
        try:
            cur.execute("INSERT INTO supplier VALUES (:name)", {"name": new_supplier})
            conn.commit()
            conn.close()
            print(f"{Fore.CYAN}Supplier {new_supplier} successfully added to the database.{Fore.RESET}")
            choices_menu()
        except sqlite3.IntegrityError:
            print(f"{Fore.MAGENTA}Supplier already exist. Try with another name.{Fore.RESET}")
            conn.close()
            insert_supplier()
main()