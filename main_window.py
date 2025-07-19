"""
Main GUI window for the Habit Tracker application
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import webbrowser
from pixela_client import PixelaClient
from config import Config

class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.pixela_client = None
        self.current_graph_id = Config.DEFAULT_GRAPH_ID
        
        # Initialize with default values
        self.username = Config.DEFAULT_USERNAME
        self.token = Config.DEFAULT_TOKEN
        
        self.create_widgets()
        self.connect_to_pixela()
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title(Config.WINDOW_TITLE)
        self.root.geometry(Config.WINDOW_SIZE)
        self.root.minsize(*Config.WINDOW_MIN_SIZE)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
    
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Pixela Habit Tracker", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # User Configuration Section
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Username
        ttk.Label(config_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.username_var = tk.StringVar(value=self.username)
        username_entry = ttk.Entry(config_frame, textvariable=self.username_var, width=30)
        username_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Token
        ttk.Label(config_frame, text="Token:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.token_var = tk.StringVar(value=self.token)
        token_entry = ttk.Entry(config_frame, textvariable=self.token_var, show="*", width=30)
        token_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Graph ID
        ttk.Label(config_frame, text="Graph ID:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5))
        self.graph_id_var = tk.StringVar(value=self.current_graph_id)
        graph_id_entry = ttk.Entry(config_frame, textvariable=self.graph_id_var, width=30)
        graph_id_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Connect button
        connect_btn = ttk.Button(config_frame, text="Connect", command=self.connect_to_pixela)
        connect_btn.grid(row=0, column=2, rowspan=3, padx=(10, 0))
        
        # Graph Management Section
        graph_frame = ttk.LabelFrame(main_frame, text="Graph Management", padding="10")
        graph_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Create Graph Button
        create_graph_btn = ttk.Button(graph_frame, text="Create New Graph", 
                                     command=self.create_graph_dialog)
        create_graph_btn.grid(row=0, column=0, padx=(0, 10))
        
        # View Graph Button
        view_graph_btn = ttk.Button(graph_frame, text="View Graph Online", 
                                   command=self.view_graph)
        view_graph_btn.grid(row=0, column=1)
        
        # Habit Tracking Section
        tracking_frame = ttk.LabelFrame(main_frame, text="Habit Tracking", padding="10")
        tracking_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        tracking_frame.columnconfigure(1, weight=1)
        
        # Date selection
        ttk.Label(tracking_frame, text="Date:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(tracking_frame, textvariable=self.date_var)
        date_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        today_btn = ttk.Button(tracking_frame, text="Today", command=self.set_today)
        today_btn.grid(row=0, column=2)
        
        # Quantity
        ttk.Label(tracking_frame, text="Quantity:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Entry(tracking_frame, textvariable=self.quantity_var)
        quantity_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Action Buttons
        actions_frame = ttk.Frame(main_frame)
        actions_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        # Pixel management buttons
        ttk.Button(actions_frame, text="Add Pixel", command=self.add_pixel).grid(row=0, column=0, padx=5)
        ttk.Button(actions_frame, text="Update Pixel", command=self.update_pixel).grid(row=0, column=1, padx=5)
        ttk.Button(actions_frame, text="Delete Pixel", command=self.delete_pixel).grid(row=0, column=2, padx=5)
        
        # Quick action buttons
        ttk.Button(actions_frame, text="Increment", command=self.increment_pixel).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(actions_frame, text="Decrement", command=self.decrement_pixel).grid(row=1, column=1, padx=5, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def connect_to_pixela(self):
        """Connect to Pixela with current credentials"""
        try:
            self.username = self.username_var.get()
            self.token = self.token_var.get()
            self.current_graph_id = self.graph_id_var.get()
            
            if not self.username or not self.token:
                messagebox.showerror("Error", "Please enter both username and token")
                return
            
            self.pixela_client = PixelaClient(self.username, self.token)
            self.status_var.set(f"Connected to Pixela as {self.username}")
            messagebox.showinfo("Success", "Connected to Pixela successfully!")
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
            self.status_var.set("Connection failed")
    
    def create_graph_dialog(self):
        """Open dialog to create a new graph"""
        if not self.pixela_client:
            messagebox.showerror("Error", "Please connect to Pixela first")
            return
        
        dialog = GraphCreationDialog(self.root, self.pixela_client)
        if dialog.result:
            self.status_var.set("Graph created successfully")
            messagebox.showinfo("Success", "Graph created successfully!")
    
    def view_graph(self):
        """Open the graph in web browser"""
        if not self.pixela_client:
            messagebox.showerror("Error", "Please connect to Pixela first")
            return
        
        url = self.pixela_client.get_graph_url(self.current_graph_id)
        webbrowser.open(url)
        self.status_var.set(f"Opened graph {self.current_graph_id} in browser")
    
    def set_today(self):
        """Set date to today"""
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
    
    def get_formatted_date(self):
        """Convert date from YYYY-MM-DD to YYYYMMDD"""
        try:
            date_obj = datetime.strptime(self.date_var.get(), "%Y-%m-%d")
            return date_obj.strftime("%Y%m%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return None
    
    def add_pixel(self):
        """Add a new pixel"""
        if not self.pixela_client:
            messagebox.showerror("Error", "Please connect to Pixela first")
            return
        
        date = self.get_formatted_date()
        if not date:
            return
        
        result = self.pixela_client.post_pixel(
            self.current_graph_id, date, self.quantity_var.get()
        )
        
        if result["success"]:
            self.status_var.set("Pixel added successfully")
            messagebox.showinfo("Success", "Pixel added successfully!")
        else:
            messagebox.showerror("Error", f"Failed to add pixel: {result['message']}")
    
    def update_pixel(self):
        """Update an existing pixel"""
        if not self.pixela_client:
            messagebox.showerror("Error", "Please connect to Pixela first")
            return
        
        date = self.get_formatted_date()
        if not date:
            return
        
        result = self.pixela_client.update_pixel(
            self.current_graph_id, date, self.quantity_var.get()
        )
        
        if result["success"]:
            self.status_var.set("Pixel updated successfully")
            messagebox.showinfo("Success", "Pixel updated successfully!")
        else:
            messagebox.showerror("Error", f"Failed to update pixel: {result['message']}")
    
    def delete_pixel(self):
        """Delete a pixel"""
        if not self.pixela_client:
            messagebox.showerror("Error", "Please connect to Pixela first")
            return
        
        date = self.get_formatted_date()
        if not date:
            return
        
        if messagebox.askyesno("Confirm", f"Delete pixel for {self.date_var.get()}?"):
            result = self.pixela_client.delete_pixel(self.current_graph_id, date)
            
            if result["success"]:
                self.status_var.set("Pixel deleted successfully")
                messagebox.showinfo("Success", "Pixel deleted successfully!")
            else:
                messagebox.showerror("Error", f"Failed to delete pixel: {result['message']}")
    
    def increment_pixel(self):
        """Increment today's pixel"""
        if not self.pixela_client:
            messagebox.showerror("Error", "Please connect to Pixela first")
            return
        
        result = self.pixela_client.increment_pixel(self.current_graph_id)
        
        if result["success"]:
            self.status_var.set("Pixel incremented successfully")
            messagebox.showinfo("Success", "Pixel incremented successfully!")
        else:
            messagebox.showerror("Error", f"Failed to increment pixel: {result['message']}")
    
    def decrement_pixel(self):
        """Decrement today's pixel"""
        if not self.pixela_client:
            messagebox.showerror("Error", "Please connect to Pixela first")
            return
        
        result = self.pixela_client.decrement_pixel(self.current_graph_id)
        
        if result["success"]:
            self.status_var.set("Pixel decremented successfully")
            messagebox.showinfo("Success", "Pixel decremented successfully!")
        else:
            messagebox.showerror("Error", f"Failed to decrement pixel: {result['message']}")


class GraphCreationDialog:
    def __init__(self, parent, pixela_client):
        self.parent = parent
        self.pixela_client = pixela_client
        self.result = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Create New Graph")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Graph ID
        ttk.Label(main_frame, text="Graph ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.graph_id_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.graph_id_var, width=30).grid(row=0, column=1, pady=5)
        
        # Graph Name
        ttk.Label(main_frame, text="Graph Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.graph_name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.graph_name_var, width=30).grid(row=1, column=1, pady=5)
        
        # Unit
        ttk.Label(main_frame, text="Unit:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.unit_var = tk.StringVar(value="hours")
        ttk.Entry(main_frame, textvariable=self.unit_var, width=30).grid(row=2, column=1, pady=5)
        
        # Type
        ttk.Label(main_frame, text="Type:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.type_var = tk.StringVar(value="float")
        type_combo = ttk.Combobox(main_frame, textvariable=self.type_var, 
                                 values=Config.GRAPH_TYPES, state="readonly", width=27)
        type_combo.grid(row=3, column=1, pady=5)
        
        # Color
        ttk.Label(main_frame, text="Color:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.color_var = tk.StringVar(value="shibafu")
        color_combo = ttk.Combobox(main_frame, textvariable=self.color_var, 
                                  values=Config.GRAPH_COLORS, state="readonly", width=27)
        color_combo.grid(row=4, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Create", command=self.create_graph).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT, padx=5)
    
    def create_graph(self):
        """Create the graph"""
        if not all([self.graph_id_var.get(), self.graph_name_var.get(), self.unit_var.get()]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        result = self.pixela_client.create_graph(
            self.graph_id_var.get(),
            self.graph_name_var.get(),
            self.unit_var.get(),
            self.type_var.get(),
            self.color_var.get()
        )
        
        if result["success"]:
            self.result = True
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", f"Failed to create graph: {result['message']}")
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()
