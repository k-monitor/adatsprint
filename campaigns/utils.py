from PyPDF2 import PdfFileReader


def get_pdf_page_count(f):
    """
    Given a file handle to a PDF, return the number of pages in that PDF.
    If the page count can't be determined for some reason, return None
    """
    try:
        pdf = PdfFileReader(f)
        return pdf.getNumPages()
    except Exception:  # TODO: can we be more specific here?
        return None
