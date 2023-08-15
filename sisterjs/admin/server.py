import socket
import threading
import re
import os
import copy

# Response Class
class Server_Response():
    def __init__(self, status_code:int=200, content_type:str='text/plain', content=''):
        self.status_code = status_code
        self.content_type = content_type
        self.content = content

    def override_response(self, server_name:str ='unnamed server', status_code:int=200, content_type:str='text/plain', content='', keep_connection:bool=False):
        self.status_code = status_code
        self.content_type = content_type
        self.content = content
        return self.generate_response(server_name, keep_connection)

    def generate_response(self, server_name:str ='unnamed server', keep_connection:bool=False):
        connection = 'Closed'
        if keep_connection:
            connection = 'Keep-Alive'
        
        response = (
f"HTTP/1.1 {self.status_code}\r\n"
f"Server: {server_name}\r\n"
f"Content-Length: {len(self.content)}\r\n"
f"Content-Type: {self.content_type}\r\n"
f"Connection: {connection}\r\n\r\n"
        )

        if isinstance(self.content, bytes):
            print("IS BYTES") # LOG
            response = response.encode('utf-8') + self.content
        else:
            print("IS STRING") # LOG
            response += self.content
            response = response.encode('utf-8')

        return response

# Server Worker Thread
class Server_Handler(threading.Thread):
    def __init__(self, client_socket, client_address, server):
        super().__init__()
        self.server = server
        self.client_socket = client_socket
        self.client_address = client_address
        self.buffer_size = 4096

    def run(self):
        print(f"Worker Thread is handling connection from {self.client_address}") # LOG
        with self.client_socket:
            request_data = self.client_socket.recv(4096).decode('utf-8')
            response_data = self.server.response(request_data)
            self.client_socket.send(response_data)
            self.client_socket.close()

        print("Worker Thread Closed Successfully.") # LOG
    
# Main Server Class
class Server():
    def __init__(self, port:int=10000, addr:str='127.0.0.1', limit:int=5):
        self.static_counter = 1
        self.default_icon = ''.encode('utf-8')
        self.server_name = "pyster/0.1.0"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.addr = addr
        self.socket.bind((addr, self.port))
        self.socket.listen(limit)
        self.running = False
        self.routes = {}
        self.static_data = {}

        @self.route('/favicon.ico')
        def handle_favicon_route():
            return Server_Response(content_type='image/webp', content=self.default_icon)
        
    def load_static_folder(self, folder_path:str):
        # Supported files: .html, .css, .js, .webp, .json, .txt
        # File name must not contain white spaces
        # Will throw an error if not
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                route_name = os.path.join(root, filename).replace('\\', '/')
                print(route_name) # LOG

                if(route_name.find(' ') != -1):
                    raise Exception(f"File name {route_name} contains spaces. Please remove them.")

                file_type = filename.split('.')[-1]
                print(file_type) # LOG

                if file_type == 'html':
                    with open(route_name, 'r') as f:
                        reply_content = f.read()
                    generate_static_response(self, route_name, content_type='text/html', content=reply_content)

                elif file_type == 'css':
                    with open(route_name, 'r') as f:
                        reply_content = f.read()
                    generate_static_response(self, route_name, content_type='text/csv', content=reply_content)
                    
                elif file_type == 'js':
                    with open(route_name, 'r') as f:
                        reply_content = f.read()
                    generate_static_response(self, route_name, content_type='*/*', content=reply_content)
                    
                elif file_type == 'webp':
                    with open(route_name, 'rb') as f:
                        reply_content= f.read()
                    generate_static_response(self, route_name, content_type='image/webp', content=reply_content)
                    
                elif file_type == 'json':
                    with open(route_name, 'r') as f:
                        reply_content = f.read()
                    generate_static_response(self, route_name, content_type='application/json', content=reply_content)
                
                elif file_type == 'txt':
                    with open(route_name, 'r') as f:
                        reply_content = f.read()
                    generate_static_response(self, route_name, content_type='text/plain', content=reply_content)
                                    
                else:
                    raise Exception(f"File type {file_type} in static folder is not supported.")
                
                self.static_counter += 1

    def run(self):
        print(f"Server running on {self.addr}:{self.port}")
        self.running = True
        while self.running:
            client_socket, client_address = self.socket.accept()
            handler = Server_Handler(client_socket, client_address, self)
            handler.start()

    def stop(self):
        self.running = False
        self.socket.close()

    def route_setmanual(self, func, route, methods:list=['GET']):
        self.routes[route] = func
        self.routes[route].methods = methods
    
    def route(self, route, methods:list=['GET']):
        def decorator(func):
            self.routes[route] = func
            self.routes[route].methods = methods
            return func
        return decorator
            
    def error_page(self, error_code):
        def decorator(func):
            self.routes[error_code] = func
            return func
        return decorator
    
    def set_icon(self, icon_path:str):
        # Only works for webp, add other formats later
        with open(icon_path, 'rb') as f:
            self.default_icon = f.read()

        @self.route('/favicon.ico')
        def handle_favicon_route():
            return Server_Response(content_type='image/webp', content=self.default_icon)

    def response(self, request_data):
        # try:
            print("Received data:") # LOG
            print(request_data) # LOG
            
            lines = request_data.split('\r\n')
            request_line_cnt = lines[0].split(' ')
            request_type = request_line_cnt[0]
            request_content = request_line_cnt[1]
            
            print("Request type: ", end=' ') # LOG
            print(request_type) # LOG
            
            route_func = self.routes.get(request_content)

            if route_func:
                print("ROUTE FOUND") # LOG

                if not (request_type in route_func.methods):
                    print("ERROR: NOT ALLOWED") # LOG
                    if(self.routes.get(405)):
                        return self.routes.get(405)().generate_response(self.server_name, keep_connection=False)
                    return Server_Response(status_code=405, content_type='text/plain', content='405 Method Not Allowed').generate_response(self.server_name, keep_connection=False)


                print("Route function: ", end=' ') # LOG
                response = route_func()
                print(response) # LOG
                if type(response) == str:
                    response = Server_Response(content=response)                

                return response.generate_response(self.server_name, keep_connection=False)
            else:
                print("ERROR: NOT FOUND") # LOG
                if(self.routes.get(404)):
                    return self.routes.get(404)().generate_response(self.server_name, keep_connection=False)
                
                return Server_Response(status_code=404, content_type='text/plain', content='404 Not Found').generate_response(self.server_name, keep_connection=False)
        
        # except:
        #     print("ERROR: INTERNAL ERROR") # LOG
        #     if(self.routes.get(500)):
        #         return self.routes.get(500)().generate_response(self.server_name, keep_connection=False)
            
        #     return Server_Response(status_code=500, content_type='text/plain', content='500 Internal Error').generate_response(self.server_name, keep_connection=False)
        

# Functions to generate responses
def html_response(html_page:str):
    with open(html_page, 'r') as f:
        content = f.read()
    return Server_Response(content_type='text/html', content=content)

def generate_static_response(server: Server, route_name:str, content_type:str='*/*', content=''):
    @server.route('/' + route_name)
    def handle_file_route():
        return Server_Response(content_type=content_type, content=content)

if __name__ == "__main__":
    server = Server()

    @server.route('/')
    def handle_home_route():
        return html_response('home.html')
    
    @server.route('/home')
    def handle_home_route():
        return html_response('home.html')
    
    @server.route('/info')
    def handle_home_route():
        return html_response('info.html')

    @server.route('/content')
    def handle_home_route():
        return html_response('content.html')

    @server.route('/about')
    def handle_about_route():
        return "This is the about page."
        
    server.set_icon('assets/favicon.webp')
    server.load_static_folder('data')
    server.load_static_folder('scripts')
    server.load_static_folder('assets')
    
    # print(server.routes.get('/scripts/content.js')().generate_response().decode('utf-8'))
    # print(server.routes.get('/scripts/home.js')().generate_response().decode('utf-8'))
    # print(server.routes.get('/scripts/info.js'))
    print(server.routes.get('/home'))
    print(server.routes.get('/info'))


    server.run()