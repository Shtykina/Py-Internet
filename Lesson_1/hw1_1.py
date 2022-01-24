#Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
#для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json
from pprint import pprint

username = "Shtykina"
url = f"https://api.github.com/users/{username}/repos"

user_data = requests.get(url).json()

print(type(user_data))
print(f"Список публичных репозиториев пользователя {username}:")
my_list = [f"List of public repositories of the user {username}:"]
for i in range(0, len(user_data)):
    my_list.append(user_data[i]['html_url'])
    print(user_data[i]['html_url'])

with open("hw1_1.json", "w", encoding="UTF-8") as js_file:
    json.dump(my_list, js_file)
