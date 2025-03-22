import os
print(f"Reading configuration from: {os.path.abspath('database.ini')}")
with open("database.ini", "r") as file:
    print(file.read())
