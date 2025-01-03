import azure.functions as func
import logging
import pdfplumber
import io

app = func.FunctionApp()


@app.route(route="pdfextract", auth_level=func.AuthLevel.FUNCTION)
def pdfextract(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("pdfextract HTTP trigger function starting to process a request.")

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
