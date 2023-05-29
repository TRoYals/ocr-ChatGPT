import os
import configparser
import pandas as pd
import utils


### 环境变量
# Path: src/main.py
current_file_dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.dirname(current_file_dir)
output_folder = os.path.join(main_dir, "output")
static_folder = os.path.join(main_dir, "static")
user_file_folder = os.path.join(main_dir, "user_file")

config = configparser.ConfigParser()
config.read(os.path.join(main_dir, "config.ini"))

API_KEY = config.get("API", "API_KEY")
SECRET_KEY = config.get("API", "SECRET_KEY")
CHATGPT_TOKEN = config.get("API", "CHATGPT_TOKEN")


def main():
    import png2csv
    import pdf2png

    utils.initialize(output_folder)
    utils.initialize(static_folder)
    pdf2png.main()
    png2csv.main()
    return


if __name__ == "__main__":
    main()
