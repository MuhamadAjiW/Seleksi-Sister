import requests

def main():
    url = 'http://localhost:10000/api/dummydata/100/uhh/nopls?Kobokan=Aeru&Merdeka=1945'

    # Kalo mau testing GET cus aja buka http://localhost:10000 di browser

    # Testing put
    data = {'name': 'peko', 'age': 100000}
    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, json=data, headers=headers)
    print("\nPut response status code:", response.status_code)
    print("Response content:")
    print(response.text)

    data = "KONPEKOKONPEKOKONPEKO"
    headers = {'Content-Type': 'text/plain'}
    response = requests.put(url, data=data, headers=headers)
    print("\nPut response status code:", response.status_code)
    print("Response content:")
    print(response.text)

    data = {'name': 'peko', 'age': 100000}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.put(url, data=data, headers=headers)
    print("\nPut response status code:", response.status_code)
    print("Response content:")
    print(response.text)

    # Testing post
    data = {'name': 'peko', 'age': 100000}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    print("\nPost response status code:", response.status_code)
    print("Response content:")
    print(response.text)

    data = "KONPEKOKONPEKOKONPEKO"
    headers = {'Content-Type': 'text/plain'}
    response = requests.post(url, data=data, headers=headers)
    print("\nPost response status code:", response.status_code)
    print("Response content:")
    print(response.text)

    data = {'name': 'peko', 'age': 100000}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=data, headers=headers)
    print("\nPost response status code:", response.status_code)
    print("Response content:")
    print(response.text)

    # Testing delete
    data = {'name': 'peko', 'age': 100000}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.delete(url, data=data, headers=headers)
    print("\nDelete response status code:", response.status_code)
    print("Response content:")
    print(response.text)

if __name__ == "__main__":
    main()