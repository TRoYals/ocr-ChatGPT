import pandas as pd
from utils import initialize
from config import output_folder, static_folder


def main():
    import png2csv
    import pdf2png

    initialize(output_folder)
    initialize(static_folder)
    pdf2png.main()
    png2csv.main()
    return


if __name__ == "__main__":
    main()
