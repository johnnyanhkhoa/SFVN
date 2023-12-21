import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

class ExcelSearchApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Excel Search App")
        
        # Variables
        self.selected_folder = tk.StringVar()
        self.keyword = tk.StringVar()
        
        # GUI Elements
        tk.Label(master, text="Select Folder:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        tk.Entry(master, textvariable=self.selected_folder, state='disabled', width=40).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(master, text="Browse", command=self.browse_folder).grid(row=0, column=2, padx=10, pady=5)
        
        tk.Label(master, text="Enter Keyword:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        tk.Entry(master, textvariable=self.keyword, width=40).grid(row=1, column=1, padx=10, pady=5)
        
        tk.Button(master, text="Search", command=self.search_keyword).grid(row=2, column=0, columnspan=3, pady=10)
        
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder.set(folder)
    
    def search_keyword(self):
        folder_path = self.selected_folder.get()
        keyword = self.keyword.get()
        
        if not folder_path or not keyword:
            messagebox.showerror("Error", "Please select a folder and enter a keyword.")
            return
        
        try:
            results = self.search_in_files(folder_path, keyword)
            if results:
                self.show_results(results)
            else:
                messagebox.showinfo("Search Results", "No matching results found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def search_in_files(self, folder_path, keyword):
        results = []

        for filename in os.listdir(folder_path):
            if filename.startswith("~$"):
                continue
            if filename.endswith(".xlsx") or filename.endswith(".xls"):
                file_path = os.path.join(folder_path, filename)
                try:
                    with open(file_path, 'rb') as f:
                        try:
                            df = pd.read_excel(f, engine='openpyxl')
                        except Exception:
                            df = pd.read_excel(f, engine='xlrd')

                    for index, row in df.iterrows():
                        for col_name, cell_value in row.items():
                            if str(keyword).lower() in str(cell_value).lower():
                                result = {
                                    'file': filename,
                                    'row': index + 2,
                                    'column': col_name
                                }
                                results.append(result)
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

        return results
    
    def show_results(self, results):
        result_text = "\n".join([f"File: {result['file']}, Row: {result['row']}, Column: {result['column']}" for result in results])
        messagebox.showinfo("Search Results", result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelSearchApp(root)
    root.mainloop()
