"""
Pixela API client for handling all API interactions
"""

import requests
from datetime import datetime
from typing import Dict, Any, Optional

class PixelaClient:
    def __init__(self, username: str, token: str):
        self.username = username
        self.token = token
        self.base_url = "https://pixe.la/v1/users"
        self.headers = {"X-USER-TOKEN": token}
    
    def create_user(self, agree_terms: bool = True, not_minor: bool = True) -> Dict[str, Any]:
        """Create a new user account"""
        url = self.base_url
        data = {
            "token": self.token,
            "username": self.username,
            "agreeTermsOfService": "yes" if agree_terms else "no",
            "notMinor": "yes" if not_minor else "no"
        }
        
        try:
            response = requests.post(url, json=data)
            return {"success": response.status_code == 200, "message": response.text}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def create_graph(self, graph_id: str, name: str, unit: str, 
                     graph_type: str = "float", color: str = "shibafu") -> Dict[str, Any]:
        """Create a new graph"""
        url = f"{self.base_url}/{self.username}/graphs"
        data = {
            "id": graph_id,
            "name": name,
            "unit": unit,
            "type": graph_type,
            "color": color
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            return {"success": response.status_code == 200, "message": response.text}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def post_pixel(self, graph_id: str, date: str = None, quantity: str = "1") -> Dict[str, Any]:
        """Post a pixel to the graph"""
        if date is None:
            date = datetime.now().strftime("%Y%m%d")
        
        url = f"{self.base_url}/{self.username}/graphs/{graph_id}"
        data = {
            "date": date,
            "quantity": quantity
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            return {"success": response.status_code == 200, "message": response.text}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def update_pixel(self, graph_id: str, date: str, quantity: str) -> Dict[str, Any]:
        """Update an existing pixel"""
        url = f"{self.base_url}/{self.username}/graphs/{graph_id}/{date}"
        data = {"quantity": quantity}
        
        try:
            response = requests.put(url, json=data, headers=self.headers)
            return {"success": response.status_code == 200, "message": response.text}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def delete_pixel(self, graph_id: str, date: str = None) -> Dict[str, Any]:
        """Delete a pixel from the graph"""
        if date is None:
            date = datetime.now().strftime("%Y%m%d")
        
        url = f"{self.base_url}/{self.username}/graphs/{graph_id}/{date}"
        
        try:
            response = requests.delete(url, headers=self.headers)
            return {"success": response.status_code == 200, "message": response.text}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def get_pixel(self, graph_id: str, date: str) -> Dict[str, Any]:
        """Get a specific pixel"""
        url = f"{self.base_url}/{self.username}/graphs/{graph_id}/{date}"
        
        try:
            response = requests.get(url, headers=self.headers)
            return {"success": response.status_code == 200, "data": response.json() if response.status_code == 200 else None}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def get_graph_url(self, graph_id: str) -> str:
        """Get the URL to view the graph"""
        return f"https://pixe.la/v1/users/{self.username}/graphs/{graph_id}.html"
    
    def increment_pixel(self, graph_id: str) -> Dict[str, Any]:
        """Increment today's pixel"""
        url = f"{self.base_url}/{self.username}/graphs/{graph_id}/increment"
        
        try:
            response = requests.put(url, headers=self.headers)
            return {"success": response.status_code == 200, "message": response.text}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def decrement_pixel(self, graph_id: str) -> Dict[str, Any]:
        """Decrement today's pixel"""
        url = f"{self.base_url}/{self.username}/graphs/{graph_id}/decrement"
        
        try:
            response = requests.put(url, headers=self.headers)
            return {"success": response.status_code == 200, "message": response.text}
        except Exception as e:
            return {"success": False, "message": str(e)}
