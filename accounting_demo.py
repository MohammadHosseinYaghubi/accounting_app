import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os
import sys
import webbrowser

class AccountingApp:
    def __init__(self, root):
        self.root = root
        self.setup_translations()
        self.current_lang = "fa"
        self.menubutton = None  
        self.setup_ui()
        self.update_text_direction()
        self.update_all_texts()

    def setup_translations(self):
        self.translations = {
            "fa": {
                "title": "نرم‌افزار حسابداری",
                "description": ":توضیحات",
                "amount": ":مقدار",
                "type": ":نوع",
                "income": "درآمد",
                "expense": "هزینه",
                "add": "اضافه کردن",
                "profit": "نمایش سود/ضرر",
                "net": "سود/ضرر خالص:",
                "menu": "منو",
                "edit": "ویرایش",
                "delete": "حذف",
                "save": "ذخیره اطلاعات",
                "load": "بارگزاری اطلاعات",
                "error": "خطا",
                "fields_error": "لطفاً همه فیلدها را پر کنید.",
                "valid_error": "لطفاً یک مقدار معتبر وارد کنید.",
                "select_error": "لطفاً یک رکورد را انتخاب کنید.",
                "edit_title": "ویرایش تراکنش",
                "save_changes": "ذخیره تغییرات",
                "no_file": "فایل داده‌ای یافت نشد!",
                "design": " ©MH_Yaghoubi : طراحی شده توسط",
                "language": "تغییر زبان"
            },
            "en": {
                "title": "Accounting Software",
                "description": "Description:",
                "amount": "Amount:",
                "type": "Type:",
                "income": "Income",
                "expense": "Expense",
                "add": "Add",
                "profit": "Show Profit/Loss",
                "net": "Net Profit/Loss:",
                "menu": "Menu",
                "edit": "Edit",
                "delete": "Delete",
                "save": "Save Data",
                "load": "Load Data",
                "error": "Error",
                "fields_error": "Please fill all fields.",
                "valid_error": "Please enter a valid value.",
                "select_error": "Please select a record.",
                "edit_title": "Edit Transaction",
                "save_changes": "Save Changes",
                "no_file": "No data file found!",
                "design": "Designed by: ©MH_Yaghoubi",
                "language": "Change Language"
            }
        }

    def _(self, key):
        return self.translations[self.current_lang].get(key, key)

    def setup_ui(self):
        self.root.title(self._("title"))
        self.set_window_geometry(600, 600)
        self.root.resizable(0, 0)
        self.root.configure(bg="#1e1e2e")

        style = ttk.Style()
        style.theme_use('clam')
        self.configure_styles(style)

        # Header Frame
        self.header_frame = ttk.Frame(self.root, padding="10")
        self.header_frame.pack(fill="x", pady=10)

        # Menu
        menu_frame = ttk.Frame(self.header_frame)
        menu_frame.pack(side="right", fill="y", padx=10)

        # Input Frame
        input_frame = ttk.Frame(self.header_frame)
        input_frame.pack(side="left", fill="x", expand=True)
        
        self.create_dropdown_menu(menu_frame)
        self.create_input_widgets(input_frame)

        # Labels and Entries
        self.description_label = ttk.Label(input_frame, text=self._("description"))
        self.description_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.description_entry = ttk.Entry(input_frame, width=30)
        self.description_entry.grid(row=0, column=1, padx=5, pady=5)

        self.amount_label = ttk.Label(input_frame, text=self._("amount"))
        self.amount_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(input_frame, width=30)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        self.type_label = ttk.Label(input_frame, text=self._("type"))
        self.type_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.type_combobox = ttk.Combobox(input_frame, values=[self._("income"), self._("expense")], width=27)
        self.type_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.type_combobox.current(0)

        self.add_button = ttk.Button(input_frame, text=self._("add"), command=self.add_transaction)
        self.add_button.grid(row=3, column=1, pady=10, sticky="e")

        self.profit_button = ttk.Button(input_frame, text=self._("profit"), command=self.net_received)
        self.profit_button.grid(row=3, column=3, pady=10, padx=5, sticky="e")

        # Treeview Frame
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(tree_frame, columns=("description", "amount", "type"), 
                               show="headings", height=10, yscrollcommand=scrollbar.set)
        self.tree.heading("description", text=self._("description"))
        self.tree.heading("amount", text=self._("amount"))
        self.tree.heading("type", text=self._("type"))
        self.tree.pack(fill="both", expand=True)

        self.tree.column("description", width=200, anchor="center")
        self.tree.column("amount", width=150, anchor="center")
        self.tree.column("type", width=150, anchor="center")

        scrollbar.config(command=self.tree.yview)

        # Net Profit/Loss Label
        self.label_net = ttk.Label(self.root, text=f"{self._('net')} 0", 
                                 font=('Helvetica', 14, 'bold'), 
                                 background='#2b2c40', 
                                 foreground='#fffffe', 
                                 relief='solid', 
                                 padding=10)
        self.label_net.pack(pady=10, fill="x", padx=10,
        anchor='e' if self.current_lang == "fa" else 'w'  
        )

        # Design Label
        self.design_label = ttk.Label(
            self.root, 
            text=self._("design"), 
            font=('Helvetica', 10),
            foreground='#94a1b2',
            cursor="hand2"
        )
        self.design_label.pack(side="bottom", pady=5)
        self.design_label.bind("<Button-1>", self.open_designer_website)
        self.design_label.bind("<Enter>", lambda e: self.design_label.config(foreground='#7f5af0'))
        self.design_label.bind("<Leave>", lambda e: self.design_label.config(foreground='#94a1b2'))

    def configure_styles(self, style):
        style.configure('TFrame', background='#1e1e2e')
        style.configure('TLabel', background='#1e1e2e', foreground='#fffffe', font=('Tahoma', 12))
        style.configure('TEntry', fieldbackground='#2b2c40', foreground='#fffffe', insertcolor='#fffffe', font=('Tahoma', 12))
        style.configure('TCombobox', fieldbackground='#2b2c40', foreground='#fffffe', selectbackground='#7f5af0', font=('Tahoma', 12))
        style.configure('TButton', background='#7f5af0', foreground='#fffffe', font=('Tahoma', 12, 'bold'), borderwidth=0)
        style.map('TButton', background=[('active', '#6247aa')], foreground=[('active', 'white')])
        style.configure('Treeview', background='#2b2c40', foreground='#fffffe', fieldbackground='#2b2c40', font=('Tahoma', 12))
        style.configure('Treeview.Heading', background='#7f5af0', foreground='#fffffe', font=('Tahoma', 12, 'bold'))
        style.map('Treeview', background=[('selected', '#7f5af0')])

    def create_dropdown_menu(self, parent):
        
        # If the previous menu exists, delete it.
        if hasattr(self, 'menubutton') and self.menubutton is not None:
            self.menubutton.destroy()
            
        # Create a new Menubutton  
        self.menubutton = ttk.Menubutton(parent, text=self._("menu"), style='TButton')
        self.menubutton.pack(side="right", anchor='ne', padx=10, pady=10)

        # Create a drop-down menu
        self.menu = tk.Menu(self.menubutton, tearoff=0)
        self.menu.configure(bg="#1e1e2e", fg="#fffffe", font=('Tahoma', 12))
       
        # Adding options to the menu with proper spacing
        menu_items = [
            (self._("edit"), self.edit_transaction),
            (self._("delete"), self.delete_transaction),
            (self._("save"), self.save_data),
            (self._("load"), self.load_data),
            ("-", None),
            (self._("language"), self.toggle_language)
        ]

        for text, command in menu_items:
            if text == "-":
                self.menu.add_separator()
            else:
                # Adding spacing to simulate right-alignment in Persian
                display_text = f"{text:>30}" if self.current_lang == "fa" else text
                self.menu.add_command(
                    label=display_text,
                    command=command
            )
        self.menubutton["menu"] = self.menu
               
        # Setting the menu direction for Windows operating system
        if self.current_lang == "fa" and 'win' in sys.platform:
            try:
                self.root.tk.call('tk', 'setPalette', 'menuBackground', '#1e1e2e')
                self.root.tk.call('tk', 'setPalette', 'menuForeground', '#fffffe')
                self.root.tk.call('tk', 'setPalette', 'menuActiveBackground', '#7f5af0')
                self.root.tk.call('tk', 'setPalette', 'menuActiveForeground', '#ffffff')
            except:
                pass       

    # Change language button
    def toggle_language(self):
        self.current_lang = "en" if self.current_lang == "fa" else "fa"
        self.update_text_direction()
        self.update_all_texts()
        self.create_dropdown_menu(self.header_frame)  

    def update_text_direction(self):
        for child in self.header_frame.winfo_children():
            child.pack_forget()
        
        # Set frame by language
        menu_frame = ttk.Frame(self.header_frame)
        input_frame = ttk.Frame(self.header_frame)
        
        if self.current_lang == "fa":
            # Persian case: menu in left & frame in right 
            menu_frame.pack(side="left", fill="y", padx=10)
            input_frame.pack(side="right", fill="x", expand=True)
        else:
            # Englisg case: menu in right & frame in left 
            menu_frame.pack(side="right", fill="y", padx=10)
            input_frame.pack(side="left", fill="x", expand=True)
        
        self.create_dropdown_menu(menu_frame)
        self.create_input_widgets(input_frame)
               
        # Update profit/loss label
        self.label_net.configure(anchor='e' if self.current_lang == "fa" else 'w')
        self.label_net.pack_configure(side='right' if self.current_lang == "fa" else 'left')
                
        # Recreate input widgets in a new frame
        self.create_input_widgets(input_frame)
                     
    def create_input_widgets(self, parent):
        """Create input widgets with appropriate layouts for each language."""
        # Delete previous widgets if they exist.
        for widget in parent.winfo_children():
            widget.destroy()
               
        # Creating labels and input fields
        self.description_label = ttk.Label(parent, text=self._("description"))
        self.description_label.grid(row=0, column=0 if self.current_lang == "en" else 2, padx=5, pady=5, sticky="e" if self.current_lang == "en" else "w")
        
        self.description_entry = ttk.Entry(parent, width=30)
        self.description_entry.grid(row=0, column=1 if self.current_lang == "en" else 1, padx=5, pady=5)

        self.amount_label = ttk.Label(parent, text=self._("amount"))
        self.amount_label.grid(row=1, column=0 if self.current_lang == "en" else 2, padx=5, pady=5, sticky="e" if self.current_lang == "en" else "w")
        
        self.amount_entry = ttk.Entry(parent, width=30)
        self.amount_entry.grid(row=1, column=1 if self.current_lang == "en" else 1, padx=5, pady=5)

        self.type_label = ttk.Label(parent, text=self._("type"))
        self.type_label.grid(row=2, column=0 if self.current_lang == "en" else 2, padx=5, pady=5, sticky="e" if self.current_lang == "en" else "w")
        
        #============
        self.type_combobox = ttk.Combobox(parent, values=[self._("income"), self._("expense")], width=27)
        self.type_combobox.grid(row=2, column=1 if self.current_lang == "en" else 1, padx=5, pady=5)
        self.type_combobox.current(0)
        #============

        self.add_button = ttk.Button(parent, text=self._("add"), command=self.add_transaction)
        self.add_button.grid(row=3, column=1 if self.current_lang == "en" else 1, pady=10, sticky="e" if self.current_lang == "fa" else "w")

        self.profit_button = ttk.Button(parent, text=self._("profit"), command=self.net_received)
        self.profit_button.grid(row=3, column=0 if self.current_lang == "en" else 2, pady=10, padx=5, sticky="w" if self.current_lang == "en" else "e")

    def update_all_texts(self):
        self.root.title(self._("title"))
        
        # Update labels
        self.description_label.config(text=self._("description"))
        self.amount_label.config(text=self._("amount"))
        self.type_label.config(text=self._("type"))
        
        # Update buttons
        self.add_button.config(text=self._("add"))
        self.profit_button.config(text=self._("profit"))
        
        # Update combobox values
        self.type_combobox.config(values=[self._("income"), self._("expense")])
        
        # Update treeview headers
        self.tree.heading("description", text=self._("description"))
        self.tree.heading("amount", text=self._("amount"))
        self.tree.heading("type", text=self._("type"))
        
        # Update menu
        self.create_dropdown_menu(self.header_frame)
        
        # Update net label
        self.net_received()
        self.label_net.configure(
        anchor='e' if self.current_lang == "fa" else 'w',
        font=('Tahoma', 14, 'bold') if self.current_lang == "fa" else ('Helvetica', 14, 'bold')
    )
        
        # Update design label
        self.design_label.config(text=self._("design"))

    def set_window_geometry(self, width, height):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)
        self.root.geometry("%dx%d+%d+%d" % (width, height, x, y))

    def open_designer_website(self, event):
        webbrowser.open_new("https://github.com/MohammadHosseinYaghubi")

    def add_transaction(self):
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        transaction_type = self.type_combobox.get()

        if description == "" or amount == "":
            messagebox.showerror(self._("error"), self._("fields_error"))
            return
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror(self._("error"), self._("valid_error"))
            return

        self.tree.insert("", tk.END, values=(description, amount, transaction_type))
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.type_combobox.current(0)
       
        
    # Transaction information change function
    def edit_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror(self._("error"), self._("select_error"))
            return

        item = self.tree.item(selected_item)
        description, amount, transaction_type = item['values']

        edit_window = tk.Toplevel(self.root)
        edit_window.title(self._("edit_title"))
        edit_window.geometry("300x200")
        edit_window.resizable(False, False)
        edit_window.configure(bg="#1e1e2e")

        ttk.Label(edit_window, text=self._("description")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        edit_description_entry = ttk.Entry(edit_window, width=30)
        edit_description_entry.grid(row=0, column=1, padx=5, pady=5)
        edit_description_entry.insert(0, description)

        ttk.Label(edit_window, text=self._("amount")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        edit_amount_entry = ttk.Entry(edit_window, width=30)
        edit_amount_entry.grid(row=1, column=1, padx=5, pady=5)
        edit_amount_entry.insert(0, amount)

        ttk.Label(edit_window, text=self._("type")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        edit_type_combobox = ttk.Combobox(edit_window, values=[self._("income"), self._("expense")], width=27)
        edit_type_combobox.grid(row=2, column=1, padx=5, pady=5)
        edit_type_combobox.set(transaction_type)

        def save_changes():
            new_description = edit_description_entry.get()
            new_amount = edit_amount_entry.get()
            new_type = edit_type_combobox.get()

            if new_description == "" or new_amount == "":
                messagebox.showerror(self._("error"), self._("fields_error"))
                return
            
            try:
                new_amount = float(new_amount)
            except ValueError:
                messagebox.showerror(self._("error"), self._("valid_error"))
                return

            self.tree.item(selected_item, values=(new_description, new_amount, new_type))
            edit_window.destroy()
            self.net_received()
            self.save_data()

        ttk.Button(edit_window, text=self._("save_changes"), command=save_changes).grid(row=3, column=1, pady=10, sticky="e")

    # Function to delete transaction information
    def delete_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror(self._("error"), self._("select_error"))
            return

        self.tree.delete(selected_item)
        self.net_received()
        self.save_data()

    # Net received calculation function
    def net_received(self):
        profit = 0
        loss = 0

        for child in self.tree.get_children():
            amount = float(self.tree.item(child, 'values')[1])
            transaction_type = self.tree.item(child, 'values')[2]

            if transaction_type == self._("income"):
                profit += amount
            elif transaction_type == self._("expense"):
                loss += amount

        net = profit - loss
        
        # Text formatting by language
        if self.current_lang == "fa":
            self.label_net.config(text=f"{self._('net')} {net:,.0f}".replace(",", "٬"))
        else:
            self.label_net.config(text=f"{self._('net')} {net}")

    # Data storage function
    def save_data(self):
        data = []
        for child in self.tree.get_children():
            description, amount, transaction_type = self.tree.item(child, 'values')
            data.append({
                "description": description,
                "amount": float(amount),
                "type": transaction_type
            })

        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    # Load data function
    def load_data(self):
        if os.path.exists("data.json"):
            with open("data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                self.tree.delete(*self.tree.get_children())
                for item in data:
                    self.tree.insert("", tk.END, values=(item["description"], item["amount"], item["type"]))
            self.net_received()
        else:
            messagebox.showinfo(self._("error"), self._("no_file"))

if __name__ == "__main__":
    root = tk.Tk()
    app = AccountingApp(root)
    root.mainloop()