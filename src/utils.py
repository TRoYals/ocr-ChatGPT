import configparser
import os
from main import main_dir
import requests
import openai
import re
import csv
import pandas as pd
import json
import shutil

config = configparser.ConfigParser()
config.read(os.path.join(main_dir, "config.ini"))

API_KEY = config.get("API", "API_KEY")
SECRET_KEY = config.get("API", "SECRET_KEY")
CHATGPT_TOKEN = config.get("API", "CHATGPT_TOKEN")

PROMPT_BASIC_INFO = config.get("PROMPT", "PROMPT_BASIC_INFO")


def chatGPT_request(content, prompt=PROMPT_BASIC_INFO, token=CHATGPT_TOKEN):
    """
    使用 GPT-3.5-turbo 模型进行对话,
    传入的 content 为用户输入的内容
    """
    openai.api_key = token
    message = f"{prompt}\n{content}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message},
        ],
    )
    answer = response.choices[0].message.content.strip()
    return answer


def extract_json_from_str(input_str):
    regex = r"\{.*?\}"

    # Try to find the first JSON object in the input string
    match = re.search(regex, input_str, re.DOTALL)

    if match is None:
        print("No JSON object found in the input string.")
        return {}

    json_str = match.group()
    try:
        # Try to parse the JSON object
        json_data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Failed to parse the JSON object: {e}")
        return {}
    return json_data


def json_to_csv(json_data, filename_path):
    """
    将 json 数据写入 csv 文件
    """
    file_exists = os.path.isfile(filename_path)
    with open(filename_path, "a", newline="") as csv_file:
        fieldnames = list(json_data.keys())  # 获取数据的键作为表头
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            # 文件不存在时写入表头
            writer.writeheader()
        writer.writerow(json_data)


def combine_xlsx(folder_path):
    """
    将指定文件夹下的所有 xlsx 文件合并为一个 xlsx 文件
    """
    combined_data = pd.DataFrame()

    files = os.listdir(folder_path)
    for file in files:
        if file.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file)
            page_df = pd.read_excel(file_path, engine="openpyxl")  # 指定解析引擎为 openpyxl
            combined_data = combined_data.append(page_df, ignore_index=True)
    combined_data.to_excel(os.path.join(folder_path, "combined.xlsx"), index=False)
    return


def get_text_from_xls_url(url):
    """
    从 xls 文件的 url 中获取文本
    """
    response = requests.get(url)
    df_header = pd.read_excel(response.content, sheet_name="header")
    df_flat_text = "###".join(df_header.to_string(index=False).split("\n"))
    df_footer = pd.read_excel(response.content, sheet_name="footer")
    df_flat_text += "###".join(df_footer.to_string(index=False).split("\n"))
    return df_flat_text


def initialize(file_path):
    """
    初始化文件夹
    """
    if os.path.exists(file_path):
        # Delete the folder and its contents if it exists
        shutil.rmtree(file_path)

    # Create an empty folder
    os.makedirs(file_path)
    return


def test():
    if " ":
        print("True")


def main():
    text = chatGPT_request(
        "XZXX cmpany is a company that sells XZXX products. June 6th"
    )
    print(text)
    print(extract_json_from_str(text))
    return


if __name__ == "__main__":
    main()
