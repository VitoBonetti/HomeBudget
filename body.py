from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3
from static_data import *

supplier_list = []


class Main:
    def __init__(self, main):

        self.setup_db()
        self.title = main.title(f"{TITLE} - {VERSION}")
        self.geometry = main.geometry(f"{main.winfo_screenwidth()}x{main.winfo_screenheight()}+0+0")

        # styling object Treeview
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background=TREEVIEW_BG, foreground=TREEVIEW_BG, rowheight=25,
                             fieldbackground=TREEVIEW_BG)
        self.style.map("Treeview", background=[("selected", TREEVIEW_SELECTED_BG)])


        # creating a menu bar
        self.menubar = Menu(main)
        main.config(menu=self.menubar)
        # file menu
        self.main_menu = Menu(self.menubar, tearoff=0)
        self.main_menu.add_command(label="Main Page", compound=LEFT)
        self.main_menu.add_separator()
        self.main_menu.add_command(label="Exit", compound=LEFT)
        self.menubar.add_cascade(label="Main", menu=self.main_menu)

        # setting up the frame for the app
        self.title_frame = LabelFrame(main, bd=0, highlightthickness=0, relief=FLAT)
        self.title_frame.pack(fill=BOTH, padx=10, pady=10)
        self.info_frame = LabelFrame(main, bd=0, highlightthickness=0, relief=FLAT)
        self.info_frame.pack(fill=BOTH, padx=10, pady=5)
        self.work_frame = LabelFrame(main, bd=0, labelanchor=N, relief=FLAT, highlightthickness=0)
        self.work_frame.pack(fill=BOTH, expand=1, padx=10, pady=5)
        self.left_work_frame = LabelFrame(self.work_frame, bd=5, relief=FLAT, highlightthickness=1)
        self.left_work_frame.pack(side=LEFT, padx=10, pady=5, anchor=NW)
        self.right_work_frame = LabelFrame(self.work_frame, bd=5, relief=FLAT, highlightthickness=1)
        self.right_work_frame.pack(side=RIGHT, padx=10, pady=5, anchor=NE, fill=BOTH, expand=1)
        self.statusbar_frame = LabelFrame(main, bd=1, relief=SUNKEN)
        self.statusbar_frame.pack(fill=BOTH, padx=0, pady=0, side=BOTTOM)

        # creating status bar
        self.statusbar_label = Label(self.statusbar_frame, text=f"{TITLE} - {VERSION}", anchor="e")
        self.statusbar_label.pack(fill=BOTH, padx=20)

        # Creating title
        self.title_label = Label(self.title_frame, font=TITLE_TEXT, text=f"{TITLE} - {VERSION}")
        self.title_label.pack(fill=BOTH, anchor=E, side=RIGHT)

        # Creating info
        self.info_label = Label(self.title_frame, font=NORMAL_TEXT, text="- test -")
        self.info_label.pack(fill=BOTH, anchor=CENTER)

        # creating a Frame that is used only on the home page. The frame will be destroyed
        # in manipulation/visualisation mode
        self.choices_frame = LabelFrame(self.title_frame, bd=0, highlightthickness=0, relief=FLAT)
        self.choices_frame.pack(fill=BOTH, anchor=CENTER, padx=10, pady=10)
        self.button_frame = LabelFrame(self.choices_frame, bd=0, highlightthickness=0, relief=FLAT)
        self.button_frame.pack()
        self.intro_label = Label(self.button_frame, text="Choose what to do", font=BOLD_TEXT)
        self.manipulation_button = Button(self.button_frame, text="Data Manipulation",
                                              command=lambda: self.go_manipulation(main))
        self.button_space = Label(self.button_frame, text=" ")
        self.visualization_button = Button(self.button_frame, text="Data Visualization", state=DISABLED)
        self.intro_label.grid(row=0, column=0, columnspan=3, sticky=NSEW, pady=10)
        self.manipulation_button.grid(row=1, column=0)
        self.button_space.grid(row=1, column=1)
        self.visualization_button.grid(row=1, column=2)

    def clear_frames(self):
        self.title_frame.forget()
        self.info_frame.forget()
        self.work_frame.forget()
        self.left_work_frame.forget()
        self.right_work_frame.forget()
        self.statusbar_frame.forget()

    def setup_db(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(CREATE_SUPPLIER_TABLE)
            self.cursor.execute(CREATE_PURCHASE_TABLE)
            self.conn.commit()
        except sqlite3.OperationalError:
            pass

    def go_manipulation(self, main):
        self.clear_frames()
        Manipulation(main)

    def handle_click(event, self, treeview):
        if treeview.identify_region(event.x, event.y) == "separator":
            return "break"

    def supplier_to_list(self):
        self.cursor.execute(SHOW_ALL_SUPPLIERS)
        for item in self.cursor.fetchall():
            supplier_list.append(item)


class Manipulation(Main):
    def __init__(self, main):
        super().__init__(main)

        def grab_date():
            date_purchase.set(calendar.get_date())

        def clear_supplier_form():
            supplier_entry.delete(0, END)

        def insert_supplier(treeview):
            if ((string_pattern.search(new_supplier.get())) is not None) or (new_supplier.get() == ""):
                messagebox.showerror("Not Valid Value", "The supplier name can contain only number and letters. "
                                                        "The field can not be empty ")
                clear_supplier_form()
            else:
                try:
                    with self.conn:
                        self.cursor.execute(INSERT_NEW_SUPPLIER, {'name': new_supplier.get()})
                        clear_supplier_form()
                except sqlite3.IntegrityError:
                    messagebox.showerror("Duplicate Supplier", "This Supplier already exist.")
                    clear_supplier_form()
                    supplier_entry.focus()
                    show_supplier_treeview(treeview)

        def show_supplier_treeview(treeview):
            self.cursor.execute(SHOW_ALL_SUPPLIERS)
            data = self.cursor.fetchall()
            global count
            count = 0
            treeview.delete(*treeview.get_children())
            for item in data:
                if count % 2 == 0:
                    treeview.insert(parent="", index="end", values=item, tags=("evenrow",))
                else:
                    treeview.insert(parent="", index="end", values=item, tags=("oddrow",))
                count += 1
            self.go_manipulation(main)

        date_purchase = StringVar()
        supplier_purchase = StringVar()
        btw9_purchase = StringVar()
        btw21_purchase = StringVar()
        statigeld_purchase = StringVar()
        discount_purchase = StringVar()
        total_amount_purchase = StringVar()
        new_supplier = StringVar()

        self.supplier_to_list()
        self.choices_frame.destroy()
        show_supplier_treeview(supplier_treeview)
        self.title_label.config(text="Insert & Delete Purchase and/or supplier")
        self.statusbar_label.config(text=f"{TITLE} - {VERSION} -- Insert & Delete Purchase and/or supplier")

        purchase_label = Label(self.left_work_frame, text="INSERT PURCHASE", font=BOLD_TEXT)
        purchase_label.grid(row=0, column=0, columnspan=4, sticky=N)
        date_label = Label(self.left_work_frame, text="Select the Date:", font=FORM_TEXT)
        date_label.grid(row=1, column=0, columnspan=4, sticky=N)
        calendar_frame = LabelFrame(self.left_work_frame, bd=0, relief=FLAT, highlightthickness=0)
        calendar_frame.grid(row=2, column=0, columnspan=4, padx=5)
        calendar = Calendar(calendar_frame, selectmode="day", year=current_year, month=current_month,
                                 day=current_day)
        calendar.pack(fill=BOTH, expand=True)
        cal_button = Button(calendar_frame, text="Get Date", command=grab_date)
        cal_button.pack(pady=2)

        supplier_pur_label = Label(self.left_work_frame, text="Supplier: ", font=FORM_TEXT)
        supplier_pur_label.grid(row=3, column=0, pady=10, sticky=W)
        supplier_combobox = ttk.Combobox(self.left_work_frame, textvariable=supplier_purchase, state="readonly",
                                         values=supplier_list, width=26)
        supplier_combobox.grid(row=3, column=1, columnspan=3, sticky=W)

        amount_9_label = Label(self.left_work_frame, text="BTW 9%: ", font=FORM_TEXT)
        amount_9_label.grid(row=4, column=0, pady=10, sticky=W)
        amount_9_entry = ttk.Entry(self.left_work_frame, textvariable=btw9_purchase, width=7)
        amount_9_entry.grid(row=4, column=1, pady=10, sticky=W)
        amount_21_label = Label(self.left_work_frame, text="BTW 21%: ", font=FORM_TEXT)
        amount_21_label.grid(row=4, column=2, pady=10, sticky=W)
        amount_21_entry = ttk.Entry(self.left_work_frame, textvariable=btw21_purchase, width=7)
        amount_21_entry.grid(row=4, column=3, pady=10, sticky=W)

        statigeld_label = Label(self.left_work_frame, text="StatiGeld: ", font=FORM_TEXT)
        statigeld_label.grid(row=5, column=0, pady=10, sticky=W)
        statigeld_entry = ttk.Entry(self.left_work_frame, textvariable=statigeld_purchase, width=7)
        statigeld_entry.grid(row=5, column=1, pady=10, sticky=W)
        discount_label = Label(self.left_work_frame, text="Discount: ", font=FORM_TEXT)
        discount_label.grid(row=5, column=2, pady=10, sticky=W)
        discount_entry = ttk.Entry(self.left_work_frame, textvariable=discount_purchase, width=7)
        discount_entry.grid(row=5, column=3, pady=10, sticky=W)
        tot_amount_label = Label(self.left_work_frame, text="Total Amount: ", font=FORM_TEXT)
        tot_amount_label.grid(row=6, column=0, pady=10, sticky=W)
        tot_amount_entry = ttk.Entry(self.left_work_frame, textvariable=total_amount_purchase, width=27)
        tot_amount_entry.grid(row=6, column=1, columnspan=3, pady=10, sticky=W)
        purchase_button_insert = Button(self.left_work_frame, text="Insert")
        purchase_button_insert.grid(row=7, column=0, columnspan=2, sticky=E, padx=10, pady=5)
        purchase_button_cancel = Button(self.left_work_frame, text="Cancel")
        purchase_button_cancel.grid(row=7, column=2, columnspan=2, sticky=W, padx=10, pady=5)

        supplier_inp_label = Label(self.left_work_frame, text="INSERT SUPPLIER", font=BOLD_TEXT)
        supplier_inp_label.grid(row=8, column=0, columnspan=4, sticky=N, pady=10, padx=5)
        supplier_label = Label(self.left_work_frame, text="Supplier: ", font=FORM_TEXT)
        supplier_label.grid(row=9, column=0, sticky=W)
        supplier_entry = ttk.Entry(self.left_work_frame, textvariable=new_supplier, width=27)
        supplier_entry.grid(row=9, column=1, columnspan=3, pady=10, sticky=W)
        supplier_button_insert = Button(self.left_work_frame, text="Insert", command=lambda: insert_supplier(supplier_treeview))
        supplier_button_insert.grid(row=10, column=0, columnspan=2, sticky=E, padx=10, pady=5)
        supplier_button_cancel = Button(self.left_work_frame, text="Cancel")
        supplier_button_cancel.grid(row=10, column=2, columnspan=2, sticky=W, padx=10, pady=5)

        # frames for the 2 treeview
        left_treeview_frame = LabelFrame(self.right_work_frame, bd=5, relief=FLAT, highlightthickness=1)
        left_treeview_frame.pack(side=LEFT, padx=10, pady=5, anchor=NW, fill=BOTH, expand=1)
        right_treeview_frame = LabelFrame(self.right_work_frame, bd=5, relief=FLAT, highlightthickness=1)
        right_treeview_frame.pack(side=RIGHT, padx=10, pady=5, anchor=NE, expand=1)

        # creating the purchase treeview
        pur_tree_scrollbar = ttk.Scrollbar(left_treeview_frame)
        pur_tree_scrollbar.pack(side=RIGHT, fill=Y)
        purchase_treeview = ttk.Treeview(left_treeview_frame, show="headings", columns=(1, 2, 3, 4, 5, 6, 7),
                                         height=5, selectmode=BROWSE, yscrollcommand=pur_tree_scrollbar.set)
        purchase_treeview.pack(side=TOP, fill=BOTH, expand=1, anchor=E)
        pur_tree_scrollbar.config(command=purchase_treeview.yview)

        purchase_treeview.column(1, anchor=CENTER, stretch=NO, width=100)
        purchase_treeview.column(2, anchor=CENTER, stretch=YES)
        purchase_treeview.column(3, anchor=CENTER, stretch=NO, width=100)
        purchase_treeview.column(4, anchor=CENTER, stretch=NO, width=100)
        purchase_treeview.column(5, anchor=CENTER, stretch=NO, width=100)
        purchase_treeview.column(6, anchor=CENTER, stretch=NO, width=100)
        purchase_treeview.column(7, anchor=CENTER, stretch=NO, width=100)

        purchase_treeview.heading(1, anchor=CENTER, text="Purchase on")
        purchase_treeview.heading(2, anchor=CENTER, text="Supplier")
        purchase_treeview.heading(3, anchor=CENTER, text="Amount 9%")
        purchase_treeview.heading(4, anchor=CENTER, text="Amount 21%")
        purchase_treeview.heading(5, anchor=CENTER, text="Statigeld")
        purchase_treeview.heading(6, anchor=CENTER, text="Discount")
        purchase_treeview.heading(7, anchor=CENTER, text="Total Amount")

        purchase_treeview.bind("<Button-1>", lambda event: Manipulation.handle_click(event, self, purchase_treeview))

        # creating the supplier treeview
        sup_tree_scrollbar = ttk.Scrollbar(right_treeview_frame)
        sup_tree_scrollbar.pack(side=RIGHT, fill=Y)
        supplier_treeview = ttk.Treeview(right_treeview_frame, show="headings", columns=(1,),
                                         height=5, selectmode=BROWSE, yscrollcommand=sup_tree_scrollbar.set)
        supplier_treeview.pack(side=TOP, fill=BOTH, expand=1, anchor=W)
        sup_tree_scrollbar.config(command=supplier_treeview.yview)
        supplier_treeview.column(1, anchor=CENTER, stretch=YES)
        supplier_treeview.heading(1, anchor=CENTER, text="Supplier")

        supplier_treeview.tag_configure("oddrow", background="black", font=BOLD_TEXT)
        supplier_treeview.tag_configure("evenrow", background="blue", font=NORMAL_TEXT)

        supplier_treeview.bind("<Button-1>", lambda event: Manipulation.handle_click(event, self, supplier_treeview))


