import os

folders = [
    "app", 
    "app/templates", 
    "app/static"
]

files = [
    "app/__init__.py",
    "app/routes.py",
    "app/models.py",
    "app/forms.py",
    "config.py",
    "run.py",
    "requirements.txt"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    with open(file, 'w') as f:
        pass

print("📁 Project structure created!")
