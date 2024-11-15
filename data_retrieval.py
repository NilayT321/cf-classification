import requests
import hashlib
from dotenv import load_dotenv
import os 
from datetime import datetime

load_dotenv()

key = os.getenv("KEY")
secret = os.getenv("SECRET")
time_stamp = datetime.now().timestamp()

print(time_stamp)
