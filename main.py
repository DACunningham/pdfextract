import pdfplumber


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


if __name__ == "__main__":
    # result = extract_data_from_pdf("fd statement 3793 31122024.pdf")
    result = extract_text_from_pdf(
        "Statement_for_01_September_2024_to_30_September_2024.pdf"
    )
