import requests

def main():
    url = 'http://localhost:5000/favvicon.ico'
    data = {'name': 'John'}

    response = requests.get(url, data=data)

    print("Get response status code:", response.status_code)
    print("Response content:")
    print(response.text)

    response = requests.post(url, data=data)

    print("Post response status code:", response.status_code)
    print("Response content:")
    print(response.text)

    response = requests.put(url, data=data)
    
    print("Put response status code:", response.status_code)
    print("Response content:")
    print(response.text)

    response = requests.delete(url, data=data)

    print("Delete response status code:", response.status_code)
    print("Response content:")
    print(response.text)

if __name__ == "__main__":
    main()