# ======================================================================================================================
# PDF pagination in batch
# ======================================================================================================================
import os
import glob
import csv
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from PyPDF4.pdf import PdfFileReader, PdfFileWriter


def create_page_pdf(num, tmp, start_page=1):
    """
    Inserts a page number into a particular PDF page
    :param num: Number of pages of the given file
    :param tmp: Temprorary PDF file
    :param start_page: Starting page number
    :return: None
    """
    PAGE_WIDTH = 215
    MARGIN_HEIGHT = 12
    c = canvas.Canvas(tmp)
    max_pages = num + 1 + start_page
    for i in range(start_page, max_pages):
        c.drawString((PAGE_WIDTH - 15) * mm, (MARGIN_HEIGHT) * mm, str(i))
        c.showPage()
    c.save()


def add_page_numbers(pdf_path, start_page=1):
    """
    Add page numbers to a pdf, save the result as a new pdf
    @param pdf_path: path to pdf
    """
    tmp = "__tmp.pdf"

    output = PdfFileWriter()
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f, strict=False)
        n = pdf.getNumPages()

        # create new PDF with page numbers
        create_page_pdf(n, tmp, start_page)

        with open(tmp, 'rb') as ftmp:
            numberPdf = PdfFileReader(ftmp)
            # iterarte pages
            for p in range(n):
                page = pdf.getPage(p)
                numberLayer = numberPdf.getPage(p)
                # merge number page with actual page
                page.mergePage(numberLayer)
                output.addPage(page)

            # write result
            if output.getNumPages():
                newpath = pdf_path[:-4] + "_numbered.pdf"
                with open(newpath, 'wb') as f:
                    output.write(f)
        os.remove(tmp)


def read_csv(csv_path):
    """
    Reads a CSV containing all the information for paginating files. It follows the structure
    - file or pattern of the PDF to be paginated
    - Starting page number that this PDF should have
    It always takes the first PDF found
    :param csv_path: The path to the CSV file containing the metadata for populating PDF with pagination
    :return: None
    """
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are ==> {", ".join(row)}')
                line_count += 1
            else:
                # print(f'\t{row[0]} - {row[1]} ')
                # Find the PDF file
                file_pattern = row[0]
                first_number = int(row[1])

                pdf_file = find_pdf(file_pattern)
                if pdf_file is not None:
                    the_path = pdf_file
                    add_page_numbers(pdf_path=the_path, start_page=first_number)

                line_count += 1
        print(f'Processed {line_count - 1} files!')

    return None


def find_pdf(pattern):
    """
    Function for finding PDFs according to a pattern
    :param pattern:
    :return:
    """
    FOLDER_PATH = os.getenv('FOLDER_PATH')
    for name in glob.glob(FOLDER_PATH + pattern + '.pdf'):
        # print(name)
        return name
    return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    csv_path = os.getenv('CSV_PATH')
    read_csv(csv_path)
