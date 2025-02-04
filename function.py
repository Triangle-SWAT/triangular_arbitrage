from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from datetime import datetime
from math import isnan
import threading
import time
import pandas
from pandas import DataFrame


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []  # Initialize variable to store candle

    def historicalData(self, reqId, bar):
        print(f'reqId: {reqId} Time: {bar.date} Close: {bar.close}')
        self.data.append([reqId, bar.date, bar.close])


ibkr_app = IBapi()
ibkr_app.connect('127.0.0.1', 7497, 10645)


def run_loop():
    ibkr_app.run()


reqId_serial = 1

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()
time.sleep(1)  # Sleep interval to allow time for connection to server
print('api_thread started')


def create_contract(curr1, curr2):
    # Create contract object
    contract = Contract()
    contract.symbol = curr1
    contract.secType = 'CASH'
    contract.exchange = 'IDEALPRO'
    contract.currency = curr2
    return contract


def request_data(app, contract):
    global reqId_serial
    reqId_serial += 1
    app.reqHistoricalData(reqId=reqId_serial, contract=contract, endDateTime='', durationStr='1 D',
                          barSizeSetting='1 day',
                          whatToShow='MIDPOINT', useRTH=0, formatDate=1, keepUpToDate=False, chartOptions=[])
    time.sleep(0.5)
    if len(app.data) == 0:
        return float('NaN')
    elif app.data[len(app.data) - 1][0] != reqId_serial:
        return float('NaN')
    else:
        return app.data[len(app.data) - 1][2]


def fetch_exc_rate(app, base, quote):
    contract = create_contract(base, quote)
    return request_data(app, contract)


def fetch_all(app, curr_list):
    matrix = DataFrame(columns=curr_list, index=curr_list)
    for i in range(0, len(curr_list)):
        for j in range(0, len(curr_list)):
            if i == j:
                matrix[curr_list[i]][curr_list[j]] = 1
            else:
                matrix[curr_list[i]][curr_list[j]] = fetch_exc_rate(app, curr_list[i], curr_list[j])
    return matrix


def fill_in_nan(matrix):
    for col in matrix.columns:
        for row in matrix.index:
            if isnan(matrix[col][row]) & (not isnan(matrix[row][col])):
                matrix[col][row] = 1 / matrix[row][col]
    return matrix


def check_all_data(matrix):
    return not matrix.isnull().values.any()


def check_arbitrage(result_dict, matrix, curr1, curr2, curr3):
    arbitrage_amount = matrix[curr1][curr2] * matrix[curr2][curr3] * matrix[curr3][curr1] - 1
    result_dict[curr1 + '.' + curr2 + '.' + curr3] = arbitrage_amount
    arbitrage_amount_rev = matrix[curr1][curr3] * matrix[curr3][curr2] * matrix[curr2][curr1] - 1
    result_dict[curr1 + '.' + curr3 + '.' + curr2] = arbitrage_amount_rev
    print(curr1 + '->' + curr2 + '->' + curr3 + '->' + curr1 + ': ' + "{:.6f}".format(arbitrage_amount))
    print(curr1 + '->' + curr3 + '->' + curr2 + '->' + curr1 + ': ' + "{:.6f}".format(arbitrage_amount_rev))
    return arbitrage_amount


def check_all_arbitrage(result_dict, matrix, currency_list):
    for i in range(0, len(currency_list)):
        for j in range(i + 1, len(currency_list)):
            for k in range(j + 1, len(currency_list)):
                check_arbitrage(result_dict, matrix, currency_list[i], currency_list[j], currency_list[k])
    return result_dict
