import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

INPUT_DIR = "input"
OUTPUT_DIR = "output"
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

temp_file = os.path.join(OUTPUT_DIR, "temp.xml")

class DayZTypeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("DayZ Type.xml Editor")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e1e")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", background="#3a3a3a", foreground="white", padding=5, font=("Arial", 10), relief="flat")
        style.map("TButton", background=[("active", "#555")])
        style.configure("TEntry", fieldbackground="#2a2a2a", foreground="white", insertcolor="white")
        style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Arial", 10))
        
        self.frame = tk.Frame(root, bg="#1e1e1e")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.search_entry = ttk.Entry(self.frame, font=("Arial", 10))
        self.search_entry.pack(fill=tk.X, padx=5, pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_items)
        
        self.listbox = tk.Listbox(self.frame, width=40, height=20, bg="#2a2a2a", fg="white", font=("Arial", 10), selectbackground="#555", relief="flat")
        self.listbox.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.details_frame = tk.Frame(self.frame, bg="#1e1e1e")
        self.details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.entries = {}
        self.fields = {
            "name": "Item name.",
            "nominal": "Maximum number of this item in the world.",
            "lifetime": "Lifetime of the item in seconds.",
            "restock": "Restock time of the item.",
            "min": "Minimum number of the item in the world.",
            "quantmin": "Minimum amount for stackable items.",
            "quantmax": "Maximum amount for stackable items.",
            "cost": "Cost value of the item for loot spawn."
        }
        
        for field, tooltip in self.fields.items():
            row = tk.Frame(self.details_frame, bg="#1e1e1e")
            row.pack(fill=tk.X, padx=5, pady=2)
            
            label = ttk.Label(row, text=field, width=15)
            label.pack(side=tk.LEFT)
            
            entry = ttk.Entry(row, font=("Arial", 10))
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            self.entries[field] = entry
            
            info_icon = ttk.Label(row, text="ⓘ", foreground="lightblue", cursor="question_arrow")
            info_icon.pack(side=tk.RIGHT, padx=5)
            info_icon.bind("<Enter>", lambda e, t=tooltip, w=info_icon: self.show_tooltip(e, t, w))
            info_icon.bind("<Leave>", self.hide_tooltip)
        
        self.tooltip = tk.Label(self.root, text="", bg="yellow", relief="solid", wraplength=200)
        self.tooltip.pack_forget()
        
        self.button_frame = tk.Frame(root, bg="#1e1e1e")
        self.button_frame.pack(fill=tk.X, pady=5)
        
        self.load_button = ttk.Button(self.button_frame, text="Load types.xml", command=self.load_xml)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        self.save_button = ttk.Button(self.button_frame, text="Save types.xml", command=self.save_xml, state=tk.DISABLED)
        self.save_button.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.X, expand=True)
        
        self.overwrite_button = ttk.Button(self.button_frame, text="Overwrite All Items", command=self.overwrite_all_items)
        self.overwrite_button.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.X, expand=True)
        
        self.tree = None
        self.filename = None
        self.current_item = None
    
    def show_tooltip(self, event, text, widget):
        x = widget.winfo_rootx() + widget.winfo_width() + 5 
        y = widget.winfo_rooty()

        self.tooltip.config(text=text)
        self.tooltip.place(x=x, y=y)
    
    def hide_tooltip(self, event):
        self.tooltip.place_forget()
    
    def search_items(self, event):
        search_term = self.search_entry.get().lower()
        self.listbox.delete(0, tk.END)
        for item in self.root_element.findall("type"):
            name = item.get("name", "Unknown")
            if search_term in name.lower():
                self.listbox.insert(tk.END, name)
    
    def load_xml(self):
        file_path = os.path.join(INPUT_DIR, "types.xml")
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "No types.xml found in input folder!")
            return
        
        try:
            self.tree = ET.parse(file_path)
            self.root_element = self.tree.getroot()
            self.tree.write(temp_file)
            self.populate_listbox()
            self.save_button["state"] = tk.NORMAL
        except ET.ParseError:
            messagebox.showerror("Error", "Invalid XML file format.")
    
    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        item_names = []
        for item in self.root_element.findall("type"):
            name = item.get("name", "Unknown")
            item_names.append(name)
        
        item_names.sort()
        
        for name in item_names:
            self.listbox.insert(tk.END, name)
    
    def on_select(self, event):
        if self.current_item:
            self.update_xml()
        
        selected_index = self.listbox.curselection()
        if not selected_index:
            return
        
        selected_name = self.listbox.get(selected_index)
        self.current_item = None
        
        for item in self.root_element.findall("type"):
            if item.get("name") == selected_name:
                self.current_item = item
                for field in self.fields:
                    if field == "name":
                        self.entries[field].delete(0, tk.END)
                        self.entries[field].insert(0, item.get("name"))
                    else:
                        element = item.find(field)
                        value = element.text if element is not None else ""
                        self.entries[field].delete(0, tk.END)
                        self.entries[field].insert(0, value)
                break
        
    def update_xml(self):
        if self.tree is None or self.current_item is None:
            return
        
        for field in self.fields:
            element = self.current_item.find(field)
            if element is not None:
                element.text = self.entries[field].get()
        
        self.tree.write(temp_file)
    
    def save_xml(self):
        if self.tree is None:
            messagebox.showerror("Error", "No XML file loaded!")
            return
        
        self.tree.write(temp_file)
        
        file_path = os.path.join(OUTPUT_DIR, "types.xml")
        self.tree.write(file_path)
        
        messagebox.showinfo("Success", "File saved successfully!")
    
    def overwrite_all_items(self):
        if self.tree is None:
            messagebox.showerror("Error", "No XML file loaded!")
            return
        
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to overwrite all items?")
        if not confirm:
            return
        
        values = {}
        for field in self.fields:
            if field == "name":
                continue
            values[field] = self.entries[field].get()
        
        for item in self.root_element.findall("type"):
            for field, value in values.items():
                element = item.find(field)
                if element is not None:
                    element.text = value
        
        self.tree.write(temp_file)
        messagebox.showinfo("Success", "All items have been overwritten!")

if __name__ == "__main__":
    root = tk.Tk()
    app = DayZTypeEditor(root)
    root.mainloop()