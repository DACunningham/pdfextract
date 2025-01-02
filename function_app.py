import azure.functions as func
import datetime
import json
import logging
import pdfplumber
import io

app = func.FunctionApp()


@app.route(route="pdfextract", auth_level=func.AuthLevel.FUNCTION)
def pdfextract(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')

    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #          "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #          status_code=200
    #     )
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
