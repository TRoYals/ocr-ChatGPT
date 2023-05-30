import os
import configparser


current_file_dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.dirname(current_file_dir)
output_folder = os.path.join(main_dir, "output")
static_folder = os.path.join(main_dir, "static")
user_file_folder = os.path.join(main_dir, "user_file")

config = configparser.ConfigParser()
config.read(os.path.join(main_dir, "config.ini"), encoding="utf-8")

API_KEY = config.get("API", "API_KEY")
SECRET_KEY = config.get("API", "SECRET_KEY")
CHATGPT_TOKEN = config.get("API", "CHATGPT_TOKEN")

PROMPT_BASIC_INFO = config.get("PROMPT", "PROMPT_BASIC_INFO")
PROMPT_SUBTABLE = config.get("PROMPT", "PROMPT_SUBTABLE")
