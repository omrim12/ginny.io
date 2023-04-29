import os
import json
import shlex
import subprocess

# create images sub directory
os.mkdir('images')
os.chdir('images')

# create kaggle api credentials
kaggle_creds_dir_path = os.path.join(os.path.expanduser('~'), '.kaggle')
kaggle_creds_path = os.path.join(kaggle_creds_dir_path, 'kaggle.json')
os.mkdir(kaggle_creds_dir_path)
api_token = {
    "username": os.environ['KAGGLE_USERNAME'],
    "key": os.environ['KAGGLE_KEY']
}
with open(kaggle_creds_path, 'w') as kaggle_creds:
    json.dump(api_token, kaggle_creds)
os.chmod(kaggle_creds_path, 600)

# download food-101 using kaggle cli
print("Downloading Food 101 datasets...")
p2 = subprocess.run(shlex.split(s="kaggle datasets download -d dansbecker/food-101"))
p3 = subprocess.run(shlex.split(s="unzip food-101.zip"))
p4 = subprocess.run(shlex.split(s="rm food-101.zip"))
