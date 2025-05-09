from google.adk.agents import Agent
import requests



def contract_fetcher(transaction_number: str) -> dict:
    """
    a tool to query contract data for a Contract Number
    """

    token = response.json()['access_token']

    print(token)

    trx_number = transaction_number.split('-', 1)[0]

    print(trx_number)

    url = f"https://da-apiservices.everestglobal.com/rns-uwsintegration/1.0/GetAccountingHistory?HeaderReference={trx_number}&currencyTypeFlag=USD"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'Ocp-Apim-Subscription-Key': 'be43725abab74da0b22417fe59bc0168',
    'X-EVE-ORIGINATOR': 'EverTechMicroServices',
    'X-EVE-CORRELATIONID': '90e6c17b-4cb0-4900-b1ea-2d516e281e78',
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    #df = pd.read_json(response.json())

    return response.json()

contract_accounting_agent = Agent(
    name="contract_accounting_agent",
    model="gemini-2.5-pro-preview-05-06",
    description="an agent to query contract data for a Contract Number",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - contract_fetcher

    The tool is used to fetch contract account data for a transaction number. Tool returns a json object with data
    in the below format:

    {
        "RIAccountant": "Victor Bevan",
        "ContractType": "XL",
        "XLContracts": {
            "HeaderContractNbr": "TP10023480-2024",
            "ContractNbr": "TP10023480-2024-1",
            "UnderwritingYear": 2024,
            "LayerName": "1ST BCO DE CHILE MRTG XL",
            "TransactionType": "Deposit Premium",
            "InstallmentDueDate": "09/30/2024",
            "PaymentBasis": "Other",
            "InstallmentPaid": "UnPaid",
            "IsPremiumAdjustment": "",
            "IsPremiumAdjustmentsBooked": "",
            "IsPremiumAdjustmentsPaid": ""
        }
    }

    Response from tool would contain multiple objects in a list. User would use this tool to query about contract. 
    Contract Number is stored with the key HeaderContractNbr. If user has not entered contract number please ask for one.
    You need to pass contract number to the tool as parameter. With the response from the tool, please answer users question.
    Some of the questions may include:
    1. How many installations are unpaid.
    2. What are the different transaction types.
    """,
    tools=[contract_fetcher],
    # tools=[get_current_time],
    # tools=[google_search, get_current_time], # <--- Doesn't work
)
