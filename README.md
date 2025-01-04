# System directions prompt 
You are an AI assistant to analyse and format data that has been extracted from UK bank statements. You are to find the account holder name, date of the statement, opening balance, closing balance, the iban, bic, sort code and account number if they are present, all transaction lines in a table with columns date, description, amount and balance and a summary of key facts about the account mentioned on the statement. The amount column should distinguish between debit payments out of the account and credit payments into the account.  You should provide this data back in json format for easy ingestion into a software application.

# Example Local API requests
curl -X POST -F 'file=@C:\Users\Dexter\source\repos\pdfextract\Statement_for_01_September_2024_to_30_September_2024.pdf' http://localhost:7071/api/pdfextract

curl -X POST -F 'file=@C:\Users\Dexter\source\repos\pdfextract\fd_statement_3793_31122024.pdf' http://localhost:7071/api/pdfextract

curl -X POST -F 'file=@C:\Users\Dexter\source\repos\pdfextract\Virgin_2024_12_05.pdf' http://localhost:7071/api/pdfextract

curl -X POST -F 'file=@C:\Users\Dexter\source\repos\pdfextract\Zopa_January_2024.pdf' http://localhost:7071/api/pdfextract

# Deployment Script
```
az group create --name MyResourceGroup --location westus

az storage account create --name mystorageaccount --location westus --resource-group MyResourceGroup --sku Standard_LRS

az functionapp create --resource-group worthit20230810162505ResourceGroup --consumption-plan-location eastus --runtime python --runtime-version 3.11 --functions-version 4 --name pdfextract-202501032128 --storage-account pdfextract --os-type Linux
```

# Deployment Guide

1. Run last step in deployment script (Once)

1. Commit chages
1. In vscode go to azure extension, pdfextract function app, RMB deploy function app
1. RMB function once complete and copy URL

# Remote Function Execution

curl -X POST -F 'file=@C:\Users\Dexter\source\repos\pdfextract\pdf_examples\Zopa_January_2024.pdf' https://pdfextract-202501032128.azurewebsites.net/api/pdfextract?code=<insert-key-here>

curl -H "x-functions-key: <insert-key-here>" -X POST -F 'file=@C:\Users\Dexter\source\repos\pdfextract\pdf_examples\Zopa_January_2024.pdf' https://pdfextract-202501032128.azurewebsites.net/api/pdfextract
