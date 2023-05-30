""".
Zoe定制内容
"""

from config import output_folder, static_folder
import os
import pandas as pd


def gpt_change_file_header(path):
    """
    调用chatGPT_request函数,将excel的表头进行对应修改
    """
    df = pd.read_excel(path, engine="openpyxl")
    headers = df.columns.tolist()
    print(headers)


def main():
    gpt_change_file_header(os.path.join(output_folder, "combined_1.xlsx"))


if __name__ == "__main__":
    main()
