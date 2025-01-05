# PDF Extract
The PDF Extract app extracts all text data from a PDF, including data within tables.  This makes it useful for extracting the text of a statement which, can then be used for further processing.

# Example Local API requests
curl -X POST -F 'file=@C:\Users\Dexter\source\repos\pdfextract\pdf_examples\Statement_for_01_September_2024_to_30_September_2024.pdf' http://localhost:7071/api/pdfextract

# Deployment Script
``` 
az group create --name MyResourceGroup --location westus

az storage account create --name mystorageaccount --location westus --resource-group MyResourceGroup --sku Standard_LRS

az functionapp create --resource-group pdfextract --consumption-plan-location uksouth --runtime python --runtime-version 3.11 --functions-version 4 --name pdfextract-202501042245 --storage-account pdfextract202501041224 --os-type Linux
```

# Deployment Guide

Run these steps one time on project startup

1. Run `py --list` and ensure version 3.11 is present.  If not install as this is the highest version of python Azure Functions supports as of 20250105.
1. Run `py -3.11 -m venv .venv`
1. Activate venv `.venv\Scripts\activate`
1. Confirm venv python version by running `python --version` then `where python`
1. Install required packages `pip install -r requirements.txt`
1. Next we need to ensure required Azure resources have been created `cd terraform`
1. Run `terraform init`

The following steps may need to be run after changes.

1. `terraform validate`
1. `terraform fmt`
1. `terraform plan`
1. `terraform apply`
1. Start Docker desktop
1. Ensure you are in the root directory of the project then, to deploy the function, run `func azure functionapp publish pdfextract-app --python --build-native-deps --build remote`


# Remote Function Execution

`curl -X POST -F 'file=@<full-pdf-file-locaiton>' https://pdfextract-app.azurewebsites.net/api/pdfextract?code=<insert-function-key>`

# Archive

#### Zip Specific Files

This loops over all files and folders in the -Path specified (in this case current working dir denoted by '.') and recursively excludes listed directories.  This is then piped into the '-Path' parameter of the `Compress-Archive` command.

```
Get-ChildItem -Path . -Recurse | Where-Object {
    # Exclude .venv, .terraform, __pycache__, *.log, .vscode, etc.
    $_.FullName -notmatch '\.venv|\.terraform|__pycache__|\.log|\.vscode|output_bin|pdf_examples|terraform'
} | Compress-Archive -DestinationPath pdfextract-app.zip
```