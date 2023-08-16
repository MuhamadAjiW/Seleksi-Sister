import requests

def main():
    url = 'http://localhost:10000/api/dummydata/100/uhh/nopls'
    data = {'name': 'peko', 'age': 100000}
    headers = {'Content-Type': 'application/json'}

    response = requests.put(url, data=data, headers=headers)
    print("Put response status code:", response.status_code)
    print("Response content:")
    print(response.text)

    data = "KONPEKOKONPEKOKONPEKO"
    headers = {'Content-Type': 'text/plain'}

    response = requests.put(url, data=data, headers=headers)
    print("Put response status code:", response.status_code)
    print("Response content:")
    print(response.text)

    data = "KONPEKOKONPEKOKONPEKO"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.put(url, data=data, headers=headers)
    print("Put response status code:", response.status_code)
    print("Response content:")
    print(response.text)

    # response = requests.get(url, data=data)

    # print("Get response status code:", response.status_code)
    # print("Response content:")
    # print(response.text)

    # response = requests.post(url, data=data)

    # print("Post response status code:", response.status_code)
    # print("Response content:")
    # print(response.text)

    # response = requests.delete(url, data=data)

    # print("Delete response status code:", response.status_code)
    # print("Response content:")
    # print(response.text)

if __name__ == "__main__":
    main()