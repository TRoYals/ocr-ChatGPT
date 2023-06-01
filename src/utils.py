import configparser
import os
import requests
import openai
import re
import csv
import pandas as pd
import json
import shutil
from io import BytesIO
from config import (
    API_KEY,
    SECRET_KEY,
    output_folder,
    static_folder,
    PROMPT_BASIC_INFO,
    PROMPT_SUBTABLE,
    CHATGPT_TOKEN,
)
import time


def chatGPT_request(
    content, prompt=PROMPT_BASIC_INFO, token=CHATGPT_TOKEN, max_attempts=3
):
    """
    使用 GPT-3.5-turbo 模型进行对话,
    传入的 content 为用户输入的内容
    """
    openai.api_key = token
    message = f"{prompt}\n{content}"
    with open(os.path.join(output_folder, "message.txt"), "a") as file:
        file.write(message)
    for attempt in range(max_attempts):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": message},
                ],
            )
            answer = response.choices[0].message.content.strip()
            with open(os.path.join(output_folder, "answer.txt"), "a") as file:
                file.write(answer)
            return answer

        except Exception as e:
            print(
                f"Request failed with exception {e}. Attempt {attempt + 1} of {max_attempts}."
            )
            if attempt + 1 == max_attempts:
                raise e
            time.sleep(1)  # Optional: add a delay before retrying the request


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


def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY,
    }
    r = requests.get(url, params=params)
    print(r.status_code)
    if r.status_code == 200:
        print(r.json()["access_token"])
        return r.json()["access_token"]
    else:
        return None


def json_to_xlsx(json_data, filename_path):
    """
    将 json 数据写入 xlsx 文件
    """
    df = pd.DataFrame(json_data, index=[0])  # 将json数据转换为DataFrame

    if os.path.isfile(filename_path):
        # 如果文件已存在，打开文件并追加数据
        with pd.ExcelWriter(filename_path, engine="openpyxl", mode="a") as writer:
            df.to_excel(writer, index=False, header=False)
    else:
        # 如果文件不存在，创建新文件并写入数据
        df.to_excel(filename_path, index=False)


def json_to_csv(json_data, filename_path):
    """
    将 json 数据写入 xlsx 文件
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
    combined_datas = []
    files = sorted(os.listdir(folder_path))
    for file in files:
        if file.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file)
            page_df = pd.read_excel(file_path, engine="openpyxl")
            if not combined_datas:
                combined_datas.append(page_df)
                continue

            found_match = False
            for i, combined in enumerate(combined_datas):
                # If the columns match, append to the dataframe and set the flag
                if (
                    len(combined.columns) == len(page_df.columns)
                    and (combined.columns == page_df.columns).all()
                ):
                    combined_datas[i] = pd.concat(
                        [combined, page_df], ignore_index=True
                    )
                    found_match = True
                    break

            if not found_match:
                combined_datas.append(page_df)

    # Save each dataframe to a separate excel file
    for i, combined in enumerate(combined_datas, 1):
        combined.to_excel(os.path.join(folder_path, f"combined_{i}.xlsx"), index=False)


def get_text_from_xls_url(url):
    """
    从 xls 文件的 url 中获取文本
    """
    response = requests.get(url)
    content = response.content

    df_flat_text = ""

    try:
        df_header = pd.read_excel(BytesIO(content), sheet_name="header")
        # 如果header不为空，加入到df_flat_text中
        if not df_header.empty:
            df_flat_text += "###".join(df_header.to_string(index=False).split("\n"))
    except Exception as e:
        print(f"Error while reading 'header' sheet: {e}")

    try:
        df_footer = pd.read_excel(BytesIO(content), sheet_name="footer")
        # 如果footer不为空，加入到df_flat_text中
        if not df_footer.empty:
            df_flat_text += "###".join(df_footer.to_string(index=False).split("\n"))
    except Exception as e:
        print(f"Error while reading 'footer' sheet: {e}")

    return df_flat_text


def remove_table_with_header(path, clean_header):
    df = pd.read_excel(path)
    if isinstance(clean_header, list):
        df = df.drop(columns=[col for col in clean_header if col in df.columns])
    elif isinstance(clean_header, str):
        if clean_header in df.columns:
            df = df.drop(columns=clean_header)
    df.to_excel(path, index=False)
    return path


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


def change_header_with_dict(list, dict):
    """
    用字典替换列表中的元素
    """
    for i in range(len(list)):
        if list[i] in dict.keys():
            list[i] = dict[list[i]]
    return list


def seprate_xlsx(file_path):
    df = pd.read_excel(file_path, engine="openpyxl")

    # 确保所有的列名都是字符串类型
    df.columns = df.columns.astype(str)

    # 初始化列表，用于保存拆分出的子表格
    tables = []

    # 设置循环，最大迭代次数为原始表格的行数（保证不会陷入无限循环）
    for i in range(df.shape[0]):
        # 检查是否还存在以"Unnamed"开头的列
        unnamed_cols = [col for col in df.columns if "Unnamed" in col]
        if not unnamed_cols:
            # 如果不存在，将剩余的表格添加到列表中并跳出循环
            df = df.dropna(axis=1, how="all")
            tables.append(df)
            break

        # 查找第一个"Unnamed"列下的第一个非空元素的位置
        for col in unnamed_cols:
            split_row = df[col].first_valid_index()
            if split_row is not None:
                break

        # 按照找到的行号将表格分成两部分，并将第一部分（新的子表格）添加到列表中
        new_table = df.iloc[:split_row].copy()
        new_table.dropna(axis=1, how="all", inplace=True)
        tables.append(new_table)

        # 更新df为剩下的部分
        df = df.iloc[split_row:].copy()

        # 将新的表头行设为表头，并确保所有的列名都是字符串类型
        df.columns = df.iloc[0].astype(str)
        df = df[1:]
        # 将所有子表格保存为新的Excel文件
        # 将所有子表格保存为新的Excel文件
    for i, table in enumerate(tables, start=0):
        filename, file_extension = os.path.splitext(os.path.basename(file_path))
        if i == 0:
            new_filename = f"{filename}{file_extension}"
        else:
            new_filename = f"{filename}-{i}{file_extension}"
        new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
        table.to_excel(new_file_path, index=False)


def main():
    text = chatGPT_request(
        "XZXX cmpany is a company that sells XZXX products. June 6th"
    )
    print(text)
    print(extract_json_from_str(text))
    return


if __name__ == "__main__":
    combine_xlsx(output_folder)
