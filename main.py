import pdfplumber
import logging
import io
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("PDF extraction function processed a request.")

    if not req.files:
        return func.HttpResponse("Malformed request, missing 'files'", status_code=400)
    file = req.files.get("file")
    if not file:
        return func.HttpResponse(
            "Please pass a PDF file in the request", status_code=400
        )

    try:
        text = ""
        with pdfplumber.open(io.BytesIO(file.read())) as pdf:
            for page in pdf.pages:
                text += page.extract_text()

        return func.HttpResponse(text, mimetype="text/plain")
    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)


# if __name__ == "__main__":
#     # result = extract_data_from_pdf("fd statement 3793 31122024.pdf")
#     result = main("Statement_for_01_September_2024_to_30_September_2024.pdf")
