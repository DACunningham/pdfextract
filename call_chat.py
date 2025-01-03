import os
import base64
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


def call_openai(pdf_text):
    endpoint = os.getenv("ENDPOINT_URL", "https://worthit-test.openai.azure.com/")
    deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

    # Initialize Azure OpenAI client with Entra ID authentication
    # token_provider = get_bearer_token_provider(
    #     DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    # )

    # client = AzureOpenAI(
    #     azure_endpoint=endpoint,
    #     azure_ad_token_provider=token_provider,
    #     api_version="2024-05-01-preview",
    # )
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=subscription_key,
        api_version="2024-05-01-preview",
    )

    # IMAGE_PATH = "YOUR_IMAGE_PATH"
    # encoded_image = base64.b64encode(open(IMAGE_PATH, "rb").read()).decode("ascii")
    chat_prompt = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are an AI assistant to analyse and format data that has been extracted from UK bank statements. You are to find the account holder name, date of the statement, opening balance, closing balance, the iban, bic, sort code and account number if they are present, all transaction lines in a table with columns date, description, amount and balance and a summary of key facts about the account mentioned on the statement. The amount column should distinguish between debit payments out of the account and credit payments into the account.  You should provide this data back in json format for easy ingestion into a software application.",
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "\"The best way to call or chat with us is via the\\n'Support' section of the Chase app.\\nAlternatively, you can call on 0800 376 3333\\n(or +44 203 493 0829 if you're abroad) or write\\nto us at PO Box 17507, Edinburgh, EH12 1PX\\nDexter Ashley Cunningham\\n15 Lyrical Way\\nHemel Hempstead\\nHP1 3HZ\\nDexter's Account statement Account number: 14579365\\nSort code: 60-84-07\\n01 September 2024 - 30 September 2024\\nOpening balance Money in Money out Closing balance\\n+ − =\\n£1,112.26 £501.11 £425.20 £1,188.17\\nDate Transaction details Amount Balance\\n01 Sep 2024 Opening balance £1,112.26\\n01 Sep 2024 Interest earned +£0.11 £1,112.37\\nInterest\\n02 Sep 2024 Round up -£0.70 £1,111.67\\nTransfer\\n03 Sep 2024 Wickes -£27.30 £1,084.37\\nPurchase\\n03 Sep 2024 To Kerrie Ruddle - Rubbish pick-up -£37.50 £1,046.87\\nPayment\\n08 Sep 2024 Boxmoor Barbers -£22.00 £1,024.87\\nPurchase\\n12 Sep 2024 To Kerrie Ruddle - Watch straps -£8.00 £1,016.87\\nPayment\\n13 Sep 2024 Round up -£0.01 £1,016.86\\nTransfer\\n14 Sep 2024 Round up -£0.35 £1,016.51\\nTransfer\\n14 Sep 2024 LinkedIn -£29.99 £986.52\\nPurchase\\nPage 1 of 4Dexter's Account statement Account number: 14579365\\nSort code: 60-84-07\\n01 September 2024 - 30 September 2024\\nDate Transaction details Amount Balance\\n15 Sep 2024 Wickes -£30.65 £955.87\\nPurchase\\n16 Sep 2024 To Nicola King - Dex for Andy bday -£23.00 £932.87\\nPayment\\n16 Sep 2024 To Kerrie Ruddle - Indian -£29.00 £903.87\\nPayment\\n16 Sep 2024 The Maltings Shopping -£2.00 £901.87\\nPurchase\\n18 Sep 2024 Round up -£0.40 £901.47\\nTransfer\\n19 Sep 2024 Trainline -£35.60 £865.87\\nPurchase\\n21 Sep 2024 To Kerrie Ruddle - Kitchen renovation -£45.00 £820.87\\nPayment\\n21 Sep 2024 B & Q -£50.00 £770.87\\nPurchase\\n22 Sep 2024 Round up -£0.41 £770.46\\nTransfer\\n23 Sep 2024 Screwfix -£7.59 £762.87\\nPurchase\\n26 Sep 2024 Round up -£0.10 £762.77\\nTransfer\\n26 Sep 2024 Round up -£0.65 £762.12\\nTransfer\\n26 Sep 2024 Round up -£0.01 £762.11\\nTransfer\\n27 Sep 2024 From CUNNINGHAM D - FD TX FOR CSH BACK +£501.00 £1,263.11\\nPayment\\n27 Sep 2024 Round up -£0.75 £1,262.36\\nTransfer\\nPage 2 of 4Dexter's Account statement Account number: 14579365\\nSort code: 60-84-07\\n01 September 2024 - 30 September 2024\\nDate Transaction details Amount Balance\\n27 Sep 2024 Saba Uk -£15.00 £1,247.36\\nPurchase\\n27 Sep 2024 The Dining Room -£7.90 £1,239.46\\nPurchase\\n27 Sep 2024 The Dining Room -£6.35 £1,233.11\\nPurchase\\n27 Sep 2024 McDonald's -£7.99 £1,225.12\\nPurchase\\n27 Sep 2024 Round up -£0.01 £1,225.11\\nTransfer\\n28 Sep 2024 Peabodys Coffee -£6.25 £1,218.86\\nPurchase\\n28 Sep 2024 Dropbox -£9.99 £1,208.87\\nPurchase\\n28 Sep 2024 Saba Uk -£15.00 £1,193.87\\nPurchase\\n29 Sep 2024 Saba Uk -£5.00 £1,188.87\\nPurchase\\n30 Sep 2024 Round up -£0.70 £1,188.17\\nTransfer\\n30 Sep 2024 Closing balance £1,188.17\\nPage 3 of 4Dexter's Account statement Account number: 14579365\\nSort code: 60-84-07\\n01 September 2024 - 30 September 2024\\nDate Transaction details Amount Balance\\nSome useful information\\nSome transactions may take a few days to finalise. This means that they may appear on your statement at a later date than when\\nyou made them.\\nForeign currency transactions\\nWhen you make foreign currency transactions, we’ll show you the conversion rate we used at the time the transaction was finalised.\\nInterest\\nThe AER is 0% (variable). AER is the rate of interest you earn from us on any balance above £0. It's short for Annual Equivalent Rate\\nand shows how much interest you’ll earn on your balance each year, including any prior interest payments.\\nYour deposit is eligible for protection by the Financial Services Compensation Scheme (FSCS).\\nThe information sheet and exclusions list are available to view in the app. For further information about the compensation provided by the FSCS, refer\\nto the FSCS website at https://www.fscs.org.uk/\\nChase is a registered trademark and trading name of J.P. Morgan Europe Limited. J.P. Morgan Europe Limited is authorised by the Prudential\\nRegulation Authority and regulated by the Financial Conduct Authority and the Prudential Regulation Authority. Our Financial Services Register\\nnumber is 124579. Registered in England & Wales with company number 938937. Our registered office is 25 Bank Street, Canary Wharf, London, E14\\n5JP, United Kingdom.\\nPage 4 of 4\"",
                }
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": '{\n    "account_holder": "",\n    "statement_date": "", // if there are 2 dates, only select the latest date here.\n    "opening_balance": 0.0,\n    "closing_balance": 0.0,\n    "account_number": "",\n    "sort_code": "",\n    "iban": "",\n    "bic": "",\n    "transactions": [\n        {\n            "date": "",\n            "description": "",\n            "amount": 0.0,\n            "balance": 0.0\n        },\n        {\n            "date": "",\n            "description": "",\n            "amount": 0.0,\n            "balance": 0.0\n        }\n    ],\n    "summary": {\n        // the key value pairs in the summary can be variable as it will change depending on the statement being read.\n    }\n}',
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": pdf_text,
                }
            ],
        },
    ]

    # chat_prompt = [
    #     {
    #         "role": "system",
    #         "content": "You are an AI assistant to analyse and format data that has been extracted from UK bank statements. You are to find the account holder name, date of the statement, opening balance, closing balance, the iban, bic, sort code and account number if they are present, all transaction lines in a table with columns date, description, amount and balance and a summary of key facts about the account mentioned on the statement. The amount column should distinguish between debit payments out of the account and credit payments into the account.  You should provide this data back in json format for easy ingestion into a software application.",
    #     },
    #     {"role": "user", "content": pdf_text},
    # ]

    # Include speech result if speech is enabled
    messages = chat_prompt

    completion = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=10000,
        temperature=0.25,
        top_p=0.3,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False,
    )  # type: ignore

    # print(completion.to_json())
    return completion.to_json()
