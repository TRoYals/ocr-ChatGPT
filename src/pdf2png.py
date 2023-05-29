from main import static_folder, user_file_folder
import fitz
import os


def pdf_to_images(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    zoom_x = 4.0  # 设置缩放系数
    zoom_y = 4.0
    mat = fitz.Matrix(zoom_x, zoom_y)  # 创建转换矩阵

    for i in range(len(doc)):
        pix = doc.get_page_pixmap(i, matrix=mat)
        image_path = os.path.join(output_folder, f"{i}.png")
        pix.save(image_path)


def main():
    target_folder = user_file_folder
    for file_name in os.listdir(target_folder):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(target_folder, file_name)
            pdf_to_images(file_path, static_folder)


if __name__ == "__main__":
    main()
