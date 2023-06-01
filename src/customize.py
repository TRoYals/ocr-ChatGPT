""".
Zoe定制内容
"""

from config import output_folder, static_folder, PROMPT_ZOE, main_dir
import os
import pandas as pd
from utils import chatGPT_request, change_header_with_dict, extract_json_from_str


def get_excel_header(path):
    """
    调用chatGPT_request函数,将excel的表头进行对应修改
    """
    df = pd.read_excel(path, engine="openpyxl")
    headers = df.columns.tolist()

    return headers


def change_header(path, prompt, new_path=False):
    df = pd.read_excel(path, engine="openpyxl")
    headers = df.columns.tolist()

    headers_mapped = gpt_get_mapped_header(headers, prompt)
    df.columns = headers_mapped
    if new_path:
        df.to_excel(new_path, index=False)
    else:
        df.to_excel(path, index=False)
    return


def gpt_get_mapped_header(header_list, prompt):
    gpt_res = chatGPT_request(header_list, prompt)
    json_from_res = extract_json_from_str(gpt_res)
    header_mapped = change_header_with_dict(header_list, json_from_res)
    return header_mapped


def excel_format_zoe_need_step1(path, new_path):
    """
    将excel的格式转换为zoe需要的格式, 第一步把表格按数字分割
    """
    df = pd.read_excel(path, engine="openpyxl")
    headers = df.columns.tolist()
    id_vars = [x for x in headers if not isinstance(x, (int, float))]

    df_melted = df.melt(
        id_vars=id_vars,
        var_name="weight_class",
        value_name="value",
    )
    df_melted.sort_values(by=id_vars, inplace=True)
    df_melted.to_excel(new_path, index=False)
    return


def excel_format_zoe_need_step2(path, info_path):
    """
    合并两个表
    """
    target_df = pd.read_excel(path, engine="openpyxl")
    info_df = pd.read_excel(info_path, engine="openpyxl")
    date, reference_no, contact_person, email = info_df.iloc[0]
    target_df["date"] = date
    target_df["reference_no"] = reference_no
    target_df["contact_person"] = contact_person
    target_df["email"] = email
    target_df.to_excel(path, index=False)
    return


def merge_excel(path):
    merged_data = pd.DataFrame()

    files = os.listdir(path)
    for file in files:
        df = pd.read_excel(os.path.join(path, file))

        # 将当前Excel文件的数据合并到总体数据中
        merged_data = merged_data.append(df, ignore_index=True)
    merged_data.to_excel(os.path.join(path, "merged.xlsx"), index=False)


def main():
    change_header(os.path.join(output_folder, "combined_1.xlsx"), PROMPT_ZOE)
    excel_format_zoe_need_step1(
        os.path.join(output_folder, "combined_1.xlsx"),
        os.path.join(output_folder, "formatted.xlsx"),
    )
    excel_format_zoe_need_step2(
        os.path.join(output_folder, "formatted.xlsx"),
        os.path.join(output_folder, "basic_info.xlsx"),
    )
    return


if __name__ == "__main__":
    merge_excel(os.path.join(main_dir, "output2"))
