__author__ = 'Max'
from Pyiiko.server import *
import requests
import datetime
import json
iiko = IikoServer()
token = iiko.token()
try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept': 'application/json'
        }
    urls = iiko.address + 'api/v2/reports/olap/columns?key='+token #+'&reportType=SALES'
    urls2 =iiko.address + 'api/v2/reports/olap?key='+token #+'&reportType=SALES'
    response2 = (requests.post(urls2,
        json={
            "reportType": "SALES",
            "groupByRowFields": [
                "DeletedWithWriteoff",
                "OrderDeleted",
                "Department",
                "OpenDate.Typed",
                "PayTypes.IsPrintCheque"
            ],
            "groupByColFields": [],
            "aggregateFields": [
                "UniqOrderId.OrdersCount",
                "DishDiscountSumInt"
            ],
            "filters": {
                "DeletedWithWriteoff": {
                    "filterType": "IncludeValues",
                    "values": [
                        "NOT_DELETED"
                    ]
                },
                "OrderDeleted": {
                    "filterType": "IncludeValues",
                    "values": [
                        "NOT_DELETED"
                    ]
                },
                "OpenDate.Typed": {
                    "filterType": "DateRange",
                    "periodType": "CUSTOM",
                    "from": datetime.date.today().strftime('%Y-%m-%d'),
                    "to": datetime.date.today().strftime('%Y-%m-%d'),
                    "includeLow": "true",
                    "includeHigh": "true"
                },
                "PayTypes.IsPrintCheque": {
                    "filterType": "IncludeValues",
                    "values": [
                        "FISCAL"
                    ]
                }
            }
        },
        headers=headers
    ))

    for i in (response2.json()["data"]):
        print(i['Department'],i['DishDiscountSumInt'],round(i['UniqOrderId.OrdersCount'],2))


except Exception as e:
    print('!',e)



iiko.quit_token()