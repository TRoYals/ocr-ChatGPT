import pandas as pd
from utils import initialize
from config import output_folder, static_folder, user_file_folder, display_folder
import png2csv
import pdf2png
import os
from customize import *


def main():
    initialize(display_folder)
    for file in os.listdir(user_file_folder):
        file_name = os.path.splitext(file)[0]
        if file.endswith(".pdf"):
            initialize(output_folder)
            initialize(static_folder)
            pdf2png.pdf_to_images(os.path.join(user_file_folder, file), static_folder)
            png2csv.main()
            # 改变xlsx文件的header，在原文件上改变
            change_header(os.path.join(output_folder, "combined_1.xlsx"), PROMPT_ZOE)
            # 将xlsx文件的格式转换为zoe需要的格式
            excel_format_zoe_need_step1(
                os.path.join(output_folder, "combined_1.xlsx"),
                os.path.join(display_folder, f"{file_name}.xlsx"),
            )
            # 合并两个表，包含需要提取的信息
            excel_format_zoe_need_step2(
                os.path.join(display_folder, f"{file_name}.xlsx"),
                os.path.join(output_folder, "basic_info.xlsx"),
                file_name,
            )
    merge_excel(display_folder)


if __name__ == "__main__":
    main()
