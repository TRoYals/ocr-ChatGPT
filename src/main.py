import os 
import configparser
import requests
import pandas as pd



### 环境变量
# Path: src/main.py
current_file_dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.dirname(current_file_dir)
output_folder = os.path.join(main_dir,'output')
static_folder = os.path.join(main_dir,'static')

config = configparser.ConfigParser()
config.read(os.path.join(main_dir,'config.ini'))

API_KEY = config.get('API', 'API_KEY')
SECRET_KEY = config.get('API', 'SECRET_KEY')



def main():

    return 

if __name__ == '__main__':
    main()    