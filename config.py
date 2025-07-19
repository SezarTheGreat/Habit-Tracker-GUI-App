"""
Configuration settings for the Habit Tracker application
"""

class Config:
    # Pixela API Configuration
    PIXELA_BASE_URL = "https://pixe.la/v1/users"
    
    # Default values
    DEFAULT_USERNAME = "sexar"
    DEFAULT_TOKEN = "oewoeidnweondwen"  # You should change this
    DEFAULT_GRAPH_ID = "graph1"
    
    # Graph configuration options
    GRAPH_COLORS = [
        "shibafu", "momiji", "sora", "ichou", 
        "ajisai", "kuro", "gray", "black"
    ]
    
    GRAPH_TYPES = ["int", "float"]
    
    # GUI Configuration
    WINDOW_TITLE = "Pixela Habit Tracker"
    WINDOW_SIZE = "800x600"
    WINDOW_MIN_SIZE = (600, 400)
    
    # Colors
    PRIMARY_COLOR = "#4CAF50"
    SECONDARY_COLOR = "#45a049"
    ERROR_COLOR = "#f44336"
    SUCCESS_COLOR = "#4CAF50"
