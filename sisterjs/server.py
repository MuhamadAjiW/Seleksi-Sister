import socket
import re

data = [
    {'employees' : [
        {
        'name': 'Employee-1',
        'branch': 'Branch-a',
        'position': 'Position-i',
        'salary': 1000
        },
        {
        'name': 'Employee-2',
        'branch': 'Branch-b',
        'position': 'Position-ii',
        'salary': 2000
        },
        {
        'name': 'Employee-3',
        'branch': 'Branch-c',
        'position': 'Position-iii',
        'salary': 3000
        }
    ]}
]

err_bad_request = (
    "HTTP/1.1 400 BAD REQUEST\r\n"
    "Content-Type: text/html\r\n\r\n"
    """
<!DOCTYPE html>
<html>
<h1>400 Bad Request</h1>
</html>
    """
).encode('utf-8')

err_page_nf = (
    "HTTP/1.1 404 PAGE NOT FOUND\r\n"
    "Content-Type: text/html\r\n\r\n"
    """
<!DOCTYPE html>
<html>
<h1>404 Page Not Found</h1>
</html>
    """
).encode('utf-8')

err_internal_error = (
    "HTTP/1.1 500 INTERNAL ERROR\r\n"
    "Content-Type: text/html\r\n\r\n"
    """
<!DOCTYPE html>
<html>
<h1>500 Internal Error</h1>
</html>
    """
).encode('utf-8')

err_not_implemented = (
    "HTTP/1.1 501 NOT IMPLEMENTED\r\n"
    "Content-Type: text/html\r\n\r\n"
    """
<!DOCTYPE html>
<html>
<h1>501 Not Implemented</h1>
</html>
    """
).encode('utf-8')

def handle_request(client_socket):
    try:
        request_data = client_socket.recv(4096).decode('utf-8')
        print("Received data:")
        print(request_data)


        lines = request_data.split('\r\n')
        request_line_cnt = lines[0].split(' ')
        request_type = request_line_cnt[0]
        request_content = request_line_cnt[1]

        request_content_cnt = request_content.split('?')
        request_addr = request_content_cnt[0][1:]
        request_query = ''
        if len(request_content_cnt) > 1:
            request_query = request_content_cnt[1]
        
        print("Request type: ", end=' ')
        print(request_type)

        print("Request addr: ", end=' ')
        print(request_addr)

        print("Request query: ", end=' ')
        print(request_query)

        reply_content = ''
        reply_content_type = ''
        
        try:
            if request_type == 'GET':
                request_addr_cnt = request_addr.split('.')
                request_addr_name = request_addr_cnt[0]
                request_addr_type = ''
                if(len(request_addr_cnt) > 1):
                    request_addr_type = request_addr_cnt[1]
                
                print("Request addr type: ", end=' ')
                print(request_addr_type)

                if request_addr_type == '':
                    print("Fetching HTTP")
                    
                    reply_content_type = "Content-Type: text/html"

                    if(request_addr == ''):
                        with open("home.html", 'r') as f:
                            reply_content = f.read()
                            
                        response = (
                            "HTTP/1.1 302 FOUND\r\n"
                            "Location: /home\r\n\r\n"
                        ).encode('utf-8')
                    else:
                        try:
                            with open(request_addr + ".html", 'r') as f:
                                reply_content = f.read()
                        except:
                            response = err_page_nf
                            raise Exception("ERROR: REQUEST NOT FOUND")
                            
                        response = (
                            "HTTP/1.1 200 OK\r\n"
                            f"{reply_content_type}\r\n\r\n"
                            f"{reply_content}\r\n"
                        ).encode('utf-8')

                elif request_addr_type == 'ico':
                    print("Fetching icon")
                
                    reply_content_type = "Content-Type: image/webp"
                    with open(request_addr_name + ".webp", 'rb') as f:
                        reply_content = f.read()
                    
                    response = (
                        "HTTP/1.1 200 OK\r\n"
                        f"{reply_content_type}\r\n\r\n"
                    ).encode('utf-8') + reply_content
                else:
                    response = err_page_nf
                    raise Exception("ERROR: INVALID TYPE REQUEST")

            elif request_type == "POST":
                response = err_not_implemented
            
            elif request_type == "PUT":
                response = err_not_implemented
            
            elif request_type == "DELETE":
                response = err_not_implemented
                
        except Exception as e:        
            print(e.args[0])
            response = err_internal_error

    except Exception as e:
        print(e.args[0])
        response = err_bad_request


    client_socket.send(response)
    client_socket.close()
    
    print("FETCH SUCCESSFUL\n\n")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_port = 12345
    server_socket.bind(('127.0.0.1', server_port))
    server_socket.listen(5)

    print(f"Server listening on port {server_port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        handle_request(client_socket)

if __name__ == "__main__":
    main()