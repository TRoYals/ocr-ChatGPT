from utils import (
    get_access_token,
    chatGPT_request,
    json_to_xlsx,
    initialize,
)
from customize import merge_excel
from pdf2png import pdf_to_images
from config import (
    output_folder,
    static_folder,
    display_folder,
    user_file_folder,
    PROMPT_INVOICE_INFO,
)
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
    initialize(output_folder)
    initialize(static_folder)
    token = get_access_token()
    for file in os.listdir(user_file_folder):
        pdf_to_images(os.path.join(user_file_folder, file), static_folder)
    for file in os.listdir(static_folder):
        if file.endswith(".jpg") or file.endswith(".png"):
            text = jpg_to_para(token, os.path.join(static_folder, file), "")
        print(text)
        chat_answer = chatGPT_request(text, PROMPT_INVOICE_INFO)
        print(chat_answer)
        data = json.loads(chat_answer)
        json_to_xlsx(data, os.path.join(output_folder, file[:-3] + "xlsx"))

    return


def test():
    initialize(display_folder)
    token = get_access_token()
    i = 0
    for file in os.listdir(user_file_folder):
        file_name = os.path.splitext(file)[0]
        if file.endswith(".pdf"):
            initialize(output_folder)
            initialize(static_folder)
            pdf_to_images(os.path.join(user_file_folder, file), static_folder)
            for file in os.listdir(static_folder):
                i += 1
                if file.endswith(".jpg") or file.endswith(".png"):
                    text = jpg_to_para(token, os.path.join(static_folder, file), "")
                print(text)
                chat_answer = chatGPT_request(text, PROMPT_INVOICE_INFO)
                print(chat_answer)
                data = json.loads(chat_answer)
                json_to_xlsx(data, os.path.join(display_folder, f"{i}.xlsx"))

    merge_excel(display_folder)


if __name__ == "__main__":
    test()
