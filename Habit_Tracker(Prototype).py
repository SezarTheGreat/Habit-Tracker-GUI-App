#Protoype for the Habit tracker app to understand the api parameters and the api puts.

import requests
from datetime import datetime

USERNAME = "sexar"
TOKEN = "oewoeidnweondwen"
GRAPH_ID = "graph1"

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}
# To create a new user, uncomment:
# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

pixela_graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": GRAPH_ID,
    "name": "Cycling Graph",
    "unit": "hours",
    "type": "float",
    "color": "ajisai"
}

headers = {
    "X-USER-TOKEN": TOKEN
}
# To create a new graph, uncomment:
# response = requests.post(url=pixela_graph_endpoint, json=graph_config, headers=headers)
# print(response.text)

pixel_creation_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
today = datetime.now()

#To create new pixel in the pixela graph
pixel_data = {
    "date": today.strftime("%Y%m%d"),
    "quantity": "2",
}
#Uncomment to make a new pixel after updating the pixel data attributes.
# response = requests.post(url=pixel_creation_endpoint, json=pixel_data, headers=headers)
# print(response.text)

#To delete a pixel from the graph.
delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"
response = requests.delete(url=delete_endpoint,headers=headers)
print(response.text)