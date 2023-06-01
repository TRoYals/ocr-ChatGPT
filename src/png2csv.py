import json
import re
from config import API_KEY, SECRET_KEY, output_folder, static_folder
import os
import requests
import base64
import pandas as pd
import time
from utils import (
    json_to_xlsx,
    combine_xlsx,
    get_text_from_xls_url,
    chatGPT_request,
    get_access_token,
    extract_json_from_str,
    seprate_xlsx,
)


def main():
    access_token = get_access_token()
    text = " "
    for file in os.listdir(static_folder):
        if file.endswith(".jpg") or file.endswith(".png"):
            text = png_to_xlsx(
                access_token,
                os.path.join(static_folder, file),
                os.path.join(output_folder, file[:-3] + "xlsx"),
                text,
            )

    combine_xlsx(output_folder)
    basic_info = chatGPT_request(text)
    json_data = extract_json_from_str(basic_info)
    attempt = 0
    while json_data == {} and attempt < 3:
        basic_info = chatGPT_request(text)
        json_data = extract_json_from_str(basic_info)
        attempt += 1
    print(json_data)
    json_to_xlsx(json_data, os.path.join(output_folder, "basic_info.xlsx"))

    return


def process_raw_table():
    return


def png_to_xlsx(
    access_token, sample_file_path, output_csv_path, need_process_text=False
):
    with open(sample_file_path, "rb") as f:
        img_data = base64.b64encode(f.read())
    request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request"
    # 设置表格识别API URL
    url = request_url + "?access_token=" + access_token

    # 发送请求
    headers = {"content-type": "application/x-www-form-urlencoded"}
    params = {
        "image": img_data,
        "is_sync": "true",  # 如果你希望立即得到结果，设置为'true'
        "request_type": "excel",  # 输出格式，可以是'excel'或者'json'
    }
    res = requests.post(url, data=params, headers=headers)
    result = res.json()
    print(result)
    attempts = 0
    while result.get("result", {}).get("ret_msg") != "已完成":
        if attempts < 3:
            time.sleep(2)
            res = requests.post(url, data=params, headers=headers)
            result = res.json()
            print(result)
            attempts += 1
        else:
            return "Error: OCR request failed after 3 attempts."

    dataurl = result["result"]["result_data"]  # 识别完成后结果存储的 url
    response = requests.get(dataurl)
    with open(output_csv_path, "wb") as file:
        df = pd.read_excel(response.content)
        # 去除重复表头
        header = df.columns.tolist()
        df = df[~df.eq(header).all(axis=1)]
        df.to_excel(output_csv_path, index=False)
        seprate_xlsx(output_csv_path)
    if need_process_text:
        need_process_text += get_text_from_xls_url(dataurl)
        return need_process_text
        # json_string = re.search(r"\{(.*?)\}", basic_info, re.DOTALL).group()
        # json_data = json.loads(json_string)
        # json_to_csv(json_data, os.path.join(output_folder, "basic_info.csv"))


if __name__ == "__main__":
    main()
