from qbClient import AuthClient
import constants as cfg
import requests
from future.moves.urllib.parse import urlencode
import pandas as pd
import json
import csv

auth_client = AuthClient(**cfg.client_secrets)

def refresh_token():
    response = auth_client.refresh(refresh_token=cfg.refreshToken)
    return response


def getCustomerData(accessToken):
    base_url = 'https://sandbox-quickbooks.api.intuit.com'
    url = '{0}/v3/company/{1}/companyinfo/{1}'.format(base_url, cfg.qBData["realm_id"])
    auth_header = 'Bearer {0}'.format(accessToken)
    headers = {
        'Authorization': auth_header,
        'Accept': 'application/json'
    }
    data = requests.get(url, headers=headers)
    return data

def saveCustomerData(data):
    with open('Customer_Data.json', 'w') as file:
        json.dump(data.json(), file, indent=4)

def extract_company_info():
    with open('Customer_Data.json', 'r') as file:
        data = json.load(file)
    company_name = data['CompanyInfo']['CompanyName']
    company_address = data['CompanyInfo']['CompanyAddr']
    csv_data = [company_name, company_address['Line1'], company_address['City'], company_address['CountrySubDivisionCode'], company_address['PostalCode']]
    with open('company_info.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['CompanyName', 'Line1', 'City', 'CountrySubDivisionCode', 'PostalCode'])
        writer.writerow(csv_data)

    company_name = data['CompanyInfo']['CompanyName']
    company_address = data['CompanyInfo']['CompanyAddr']

    csv_data = [company_name, company_address['Line1'], company_address['City'], company_address['CountrySubDivisionCode'], company_address['PostalCode']]

    with open('company_info.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['CompanyName', 'Line1', 'City', 'CountrySubDivisionCode', 'PostalCode'])
        writer.writerow(csv_data)

if __name__ == "__main__":
    response = refresh_token()
    access_token = response["access_token"]
    customer_data = getCustomerData(accessToken=access_token)
    saveCustomerData(customer_data)
    extract_company_info()
