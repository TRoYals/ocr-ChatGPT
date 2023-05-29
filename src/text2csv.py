from utils import get_access_token, chatGPT_request, PROMPT_SUBTABLE, json_to_csv
from main import output_folder, static_folder
import os
import base64
import requests
import json


def jpg_to_para(
    access_token, sample_file_path, output_csv_path, need_process_text=False
):
    with open(sample_file_path, "rb") as f:
        img_data = base64.b64encode(f.read())
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 设置表格识别API URL
    url = request_url + "?access_token=" + access_token

    # 发送请求
    headers = {"content-type": "application/x-www-form-urlencoded"}
    params = {
        "image": img_data,
        "language_type": "CHN_ENG",
        "detect_direction": "true",
    }
    res = requests.post(url, data=params, headers=headers)
    data = res.json()
    # Get the 'words_result' list from the data
    words_result = data["words_result"]

    # Extract the 'words' field from each dictionary in 'words_result'
    words_list = [result["words"] for result in words_result]

    # Combine the 'words' into a single paragraph
    paragraph = "###".join(words_list)

    # Print the resulting paragraph
    return paragraph


def main():
    token = get_access_token()
    for file in os.listdir(static_folder):
        if file.endswith(".jpg") or file.endswith(".png"):
            text = jpg_to_para(token, os.path.join(static_folder, file), "")
        chat_answer = chatGPT_request(text, PROMPT_SUBTABLE)
        data = json.loads(chat_answer)
        for item in data["products"]:
            json_to_csv(item, os.path.join(output_folder, "subtable.csv"))
    return


def test():
    # 给定的字符串
    data_string = """
    {
    "products": [
        {
            "index": 1,
            "product_id": "P0-PROW2303-0323",
            "description": "64 PK BELLY A B/L R/L W SOFTBONES SINGLE RIBBED",
            "packing": "1 PK",
            "weight": "52.32 KGM",
            "unit_price": 8,
            "value": 418.56
        },
        {
            "index": 2,
            "product_id": "PK10000910",
            "description": "67 PK ASC LOIN B/L MULTI",
            "packing": "21.42 KGM",
            "weight": "21.42 KGM",
            "unit_price": 4.6,
            "value": 98.53
        },
        {
            "index": 3,
            "product_id": "PK10001257",
            "description": "68 PK SPARERIBS IWP 20KG/CTN FRIMESA BRZ",
            "packing": "31 KGM",
            "weight": "31 KGM",
            "unit_price": 4.9,
            "value": 151.9
        },
        {
            "index": 4,
            "product_id": "BV10003628",
            "description": "72 BF RIBEYE MONDELLI BRZ Halal",
            "packing": "22.472 KGM",
            "weight": "22.472 KGM",
            "unit_price": 11.8,
            "value": 265.17
        },
        {
            "index": 5,
            "product_id": "BV10004408",
            "description": "73 BE SHIN/SHANK MINERVA BRZ Halal",
            "packing": "30.58 KGM",
            "weight": "30.58 KGM",
            "unit_price": 6.8,
            "value": 207.94
        }
    ]
    }
    """

    # 将字符串转换为JSON数据
    data = json.loads(data_string)

    # 打印JSON数据
    print(data["products"])


if __name__ == "__main__":
    main()
