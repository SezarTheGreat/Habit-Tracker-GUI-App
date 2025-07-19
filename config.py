"""
Configuration settings for the Habit Tracker application
"""
import os

class Config:
    # Pixela API Configuration
    PIXELA_BASE_URL = "https://pixe.la/v1/users"
    
    # Default values - Using environment variables or empty defaults
    DEFAULT_USERNAME = os.getenv("PIXELA_USERNAME", "")
    DEFAULT_TOKEN = os.getenv("PIXELA_TOKEN", "")
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
