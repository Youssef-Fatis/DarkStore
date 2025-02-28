import json
from API.payload import *
from API.headers import *
import requests


class Zyda:
    def login(self, globalUrl):
        loginResponse = requests.post(
            globalUrl, data=json.dumps(loginPayload), headers=loginHeaders)
        # Check if the login was successful
        if loginResponse.status_code == 200:
            loginData = loginResponse.json()
            if 'data' in loginData and 'signIn' in loginData['data']:
                accessToken = loginData['data']['signIn']['accessToken']
                return accessToken
            else:
                print("Login response does not contain expected data.")
        else:
            print(f"Login failed: {loginResponse.status_code}")
            print(loginResponse.text)
            raise Exception(
                f"Failed To Fetch Status Code: {loginResponse.status_code}, Error: {loginResponse.text}", )

    def getOrders(self, s, globalUrl, accessToken):
        # Send the orders request
        ordersResponse = s.post(globalUrl, data=json.dumps(
            ordersPayload), headers=authHeader(accessToken))

        if ordersResponse.status_code == 200:
            # Parse and print the response
            ordersData = ordersResponse.json()
            # print(json.dumps(ordersData, indent=4))
            return ordersData
        else:
            print(f"Failed to fetch orders: {ordersResponse.status_code}")
            print(ordersResponse.text)
            raise Exception(
                f"Failed To Fetch Status Code: {ordersResponse.status_code}, Error: {ordersResponse.text}", )

    def getOrdersByName(self, s, globalUrl, accessToken, searchValue):
        # Send the orders request
        ordersResponse = s.post(globalUrl, data=json.dumps(
            getOrderByNamePayload(searchValue)), headers=authHeader(accessToken))

        if ordersResponse.status_code == 200:
            # Parse and print the response
            ordersData = ordersResponse.json()
            # print(json.dumps(ordersData, indent=4))
            return ordersData
        else:
            print(f"Failed to fetch orders: {ordersResponse.status_code}")
            print(ordersResponse.text)
            raise Exception(
                f"Failed To Fetch Status Code: {ordersResponse.status_code}, Error: {ordersResponse.text}", )

    def getOrderById(self, s, globlaUrl, accessToken, orderId):
        orderResponse = s.post(globlaUrl, data=json.dumps(
            getOrderByIdPayload(orderId)), headers=authHeader(accessToken))
        if orderResponse.status_code == 200:
            ordersData = orderResponse.json()
            # print(json.dumps(ordersData, indent=4))
            return ordersData
        else:
            print("error")
            print(f"Failed to fetch orders: {orderResponse.status_code}")
            print(orderResponse.text)
            raise Exception(
                f"Failed To Fetch Status Code: {orderResponse.status_code}, Error: {orderResponse.text}", )
