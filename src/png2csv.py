from main import API_KEY, SECRET_KEY, output_folder, static_folder
import os
import requests
import base64
import pandas as pd

def main():
    access_token = get_access_token()
    for file in os.listdir(static_folder):
        if file.endswith('.jpg') or file.endswith('.png'):
            png_to_xlsx(access_token,os.path.join(static_folder,file),os.path.join(output_folder,file[:-3]+'xlsx'))
    combine_xlsx(output_folder)
    return

def get_access_token():
    url = 'https://aip.baidubce.com/oauth/2.0/token'
    params = {
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': SECRET_KEY
    }
    r = requests.get(url, params=params)
    print(r.status_code)
    if r.status_code == 200:
        return r.json()['access_token']
    else:
        return None

def png_to_xlsx(access_token,sample_file_path,output_csv_path):
    with open(sample_file_path, 'rb') as f:
        img_data = base64.b64encode(f.read())
    request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request"
    # 设置表格识别API URL
    url = request_url + "?access_token=" + access_token

    # 发送请求
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    params = {
        'image': img_data,
        'is_sync': 'true',  # 如果你希望立即得到结果，设置为'true'
        'request_type': 'excel',  # 输出格式，可以是'excel'或者'json'
    }
    res = requests.post(url, data=params, headers=headers)

    result = res.json()
    print(result)
    dataurl = result['result']['result_data']     # 识别完成后结果存储的 url
    response =  requests.get(dataurl)
    with open(output_csv_path, 'wb') as file:
        df = pd.read_excel(response.content)
        df.to_excel(output_csv_path,index=False)

def combine_xlsx(folder_path):
    combined_data = pd.DataFrame()

    files = os.listdir(folder_path)
    for file in files:
        if file.endswith('.xlsx'):
            file_path = os.path.join(folder_path, file)
            page_df = pd.read_excel(file_path, engine='openpyxl')  # 指定解析引擎为 openpyxl
            combined_data = combined_data.append(page_df, ignore_index=True)
    combined_data.to_excel(os.path.join(folder_path,'combined.xlsx'),index=False)
    return 


if __name__ == "__main__":
    main()