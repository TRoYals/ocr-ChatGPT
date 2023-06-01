from config import user_file_folder, static_folder
import fitz
import os


def pdf_to_images(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    zoom_x = 4  # 设置缩放系数
    zoom_y = 4
    mat = fitz.Matrix(zoom_x, zoom_y)  # 创建转换矩阵

    for i in range(len(doc)):
        pix = doc.get_page_pixmap(i, matrix=mat)
        image_path = os.path.join(output_folder, f"{i}.png")
        pix.save(image_path)


def main():
    return


if __name__ == "__main__":
    main()
