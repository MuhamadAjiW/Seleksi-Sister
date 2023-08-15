from errorpages import *
import socket
import re


def get_request(request_content):
    response = err_page_nf

    request_content_cnt = request_content.split('?')
    request_addr = request_content_cnt[0][1:]
    request_query = ''
    if len(request_content_cnt) > 1:
        request_query = request_content_cnt[1]

    request_addr_cnt = request_addr.split('.')
    request_addr_name = request_addr_cnt[0]
    request_addr_type = ''
    
    if(len(request_addr_cnt) > 1):
        request_addr_type = request_addr_cnt[1]
    
    print("Request addr: ", end=' ')
    print(request_addr)

    print("Request query: ", end=' ')
    print(request_query)
    
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
                return response
                
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

    elif request_addr_type == 'js':
        print("Fetching js scripts")
    
        reply_content_type = "Content-Type: */*"
        with open(request_addr_name + ".js", 'r') as f:
            reply_content = f.read()
        
        response = (
            "HTTP/1.1 200 OK\r\n"
            f"{reply_content_type}\r\n\r\n"
            f"{reply_content}"
        ).encode('utf-8')

    elif request_addr_type == 'json':
        print("Fetching json data")
    
        reply_content_type = "Content-Type: application/json"
        with open(request_addr_name + ".json", 'r') as f:
            reply_content = f.read()
        
        response = (
            "HTTP/1.1 200 OK\r\n"
            f"{reply_content_type}\r\n\r\n"
            f"{reply_content}"
        ).encode('utf-8')

    else:
        response = err_forbidden
        return response

    return response



def handle_request(client_socket):
    try:
        request_data = client_socket.recv(4096).decode('utf-8')
        print("Received data:")
        print(request_data)


        lines = request_data.split('\r\n')
        request_line_cnt = lines[0].split(' ')
        request_type = request_line_cnt[0]
        request_content = request_line_cnt[1]
        
        print("Request type: ", end=' ')
        print(request_type)
        
        try:
            if request_type == 'GET':
                try:
                    response = get_request(request_content)
                except:
                    response = err_page_nf

            elif request_type == "POST":
                #TODO: Implement
                response = err_not_implemented
            
            elif request_type == "PUT":
                #TODO: Implement
                response = err_not_implemented
            
            elif request_type == "DELETE":
                #TODO: Implement
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