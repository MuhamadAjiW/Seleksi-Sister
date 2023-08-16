# Disclaimer dulu

# kalo ini frameworknya rada aneh maap banget
# Gw kaga ada pengalaman web samsek
# Asal jalan doang kaga tau struktur
# Maapin


import socket
import threading
import os
import json
import sqlite3
# Request Class
class Request():
    def __init__(self, reqstr:str=''):
        # print("Received data:") # LOG
        # print(reqstr) # LOG
        
        reqstr = reqstr
        area = reqstr.split('\r\n\r\n')

        infolines = area[0].split('\r\n')
        print(infolines)

        request_line = infolines[0].split(' ')
        self.type = request_line[0]
        
        print("Request type: ", end=' ') # LOG
        print(self.type) # LOG

        addr = request_line[1]
        addr_cnt = addr.split('?')

        self.addr = addr_cnt[0]
        self.query = None
        self.contents = None


        lastln = infolines[len(infolines) - 1].split(': ')
        if(lastln[0] == "Content-Type"):
            self.content_type = lastln[1]
            print("Request has content: ", end=' ') # LOG
            print(self.content_type)

            self.contents = area[1]
            print("Request contents: ") # LOG
            print(self.contents) # LOG

        if(len(addr_cnt) > 1):
            self.query = extract_query(addr_cnt[1])

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
        return self.generate(server_name, keep_connection)

    def generate(self, server_name:str ='unnamed server', keep_connection:bool=False):
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
            # print("IS BYTES") # LOG
            response = response.encode('utf-8') + self.content
        else:
            # print("IS STRING") # LOG
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
        self.config = {}

        @self.route('/favicon.ico')
        def handle_favicon_route(request):
            return Server_Response(content_type='image/webp', content=self.default_icon)
        
    def load_static_folder(self, folder_path:str):
        # Supported files: .html, .css, .js, .webp, .json, .txt
        # File name must not contain white spaces
        # Will throw an error if not satisfied
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                route_name = os.path.join(root, filename).replace('\\', '/')
                # print(route_name) # LOG

                if(route_name.find(' ') != -1):
                    raise Exception(f"File name {route_name} contains spaces. Please remove them.")

                file_type = filename.split('.')[-1]
                # print(file_type) # LOG

                if file_type == 'html':
                    generate_static_response(self, route_name, content_type='text/html', read_type='r')
                elif file_type == 'css':
                    generate_static_response(self, route_name, content_type='text/csv', read_type='r')
                elif file_type == 'js':
                    generate_static_response(self, route_name, content_type='*/*', read_type='r')
                elif file_type == 'webp':
                    generate_static_response(self, route_name, content_type='image/webp', read_type='rb')
                elif file_type == 'json':
                    generate_static_response(self, route_name, content_type='application/json', read_type='r')
                elif file_type == 'txt':
                    generate_static_response(self, route_name, content_type='text/plain', read_type='r')
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
    
    def route(self, route, methods:list=['GET']):
        if(route.find(' ') != -1):
            raise Exception(f"Route name {route} contains spaces. Please remove them.")

        def decorator(func):
            if methods == None:
                raise Exception("Methods cannot be None.")

            if route not in self.routes:
                self.routes[route] = {}
            # print("Adding method for route: ", end=' ') # LOG
            # print(route)
            for method in methods:
                # print(method) # LOG
                self.routes[route][method] = func

            def decorated_func(request: Request):
                return func(request)
            return decorated_func
        
        return decorator
            
    def error_page(self, error_code):
        def decorator(func):
            self.routes[error_code] = func
            def decorated_func(request):
                return func(request)
            return decorated_func
        return decorator
    
    def set_icon(self, icon_path:str):
        # Only works for webp, add other formats later
        with open(icon_path, 'rb') as f:
            self.default_icon = f.read()

        @self.route('/favicon.ico')
        def handle_favicon_route(request):
            return Server_Response(content_type='image/webp', content=self.default_icon)

    def response(self, request_data):
        try:
            request = Request(request_data)

            route_funcs = self.routes.get(request.addr, {})

            if route_funcs == {}:
                print("ERROR: NOT FOUND") # LOG
                if(self.routes.get(404)):
                    return self.routes.get(404)(request).generate(self.server_name, keep_connection=False)
                
                return Server_Response(status_code=404, content_type='text/plain', content='404 Not Found').generate(self.server_name, keep_connection=False)
        

            route_func = route_funcs.get(request.type)

            if route_func:
                print("ROUTE FOUND") # LOG
                    
                if request.type == 'GET':
                    response = route_func(request)
                    if type(response) == str:
                        response = Server_Response(content=response)

                    return response.generate(self.server_name, keep_connection=False)
                
                #TODO: Implement other methods
                elif request.type == 'PUT':
                    raise Exception("PUT method is not implemented yet.")
                
                elif request.type == 'POST':
                    raise Exception("POST method is not implemented yet.")

                elif request.type == 'DELETE':
                    raise Exception("DELETE method is not implemented yet.")
                
                else:
                    raise Exception(f"{request.type} method is not implemented yet.")
            
            else:
                print("ERROR: NOT ALLOWED") # LOG
                if(self.routes.get(405)):
                    return self.routes.get(405)(request).generate(self.server_name, keep_connection=False)
                return Server_Response(status_code=405, content_type='text/plain', content='405 Method Not Allowed').generate(self.server_name, keep_connection=False)

        except Exception as e:
            print("ERROR: INTERNAL ERROR") # LOG
            print(e.args)
            print(e.with_traceback) # LOG
            if(self.routes.get(500)):
                return self.routes.get(500)(request).generate(self.server_name, keep_connection=False)
            
            return Server_Response(status_code=500, content_type='text/plain', content='500 Internal Error').generate(self.server_name, keep_connection=False)
        

# Functions to generate responses
def html_response(html_page:str):
    with open(html_page, 'r') as f:
        content = f.read()
    return Server_Response(content_type='text/html', content=content)

def generate_static_response(server: Server, route_name:str, content_type:str='*/*', read_type='r'):
    @server.route('/' + route_name)
    def handle_file_route(request):
        with open(route_name, read_type) as f:
            content = f.read()
        return Server_Response(content_type=content_type, content=content)
    
def generate_data(server: Server, route_name:str, content_type:str='application/json', content=''):
    @server.route(route_name)
    def handle_file_route(request):
        return Server_Response(content_type=content_type, content=content)

def extract_query(query:str):
    query_dict = {}
    query_cnt = query.split('&')
    for query in query_cnt:
        query_pair = query.split('=')
        query_dict[query_pair[0]] = query_pair[1]
    return query_dict

# Main, contoh penggunaan
if __name__ == "__main__":
    # Penggunaannya mirip flask
    server = Server()
    
    # Returnnya harus dalam bentuk Server_Response, cuman string sama html aja yang dikhususin bisa dihandle tanpa bentuk Server_Response
    @server.route('/', methods=["GET"])
    def handle_home_route(request: Request):
        return html_response('home.html')
    
    @server.route('/home')
    def handle_home_route(request: Request):
        return html_response('home.html')
    
    @server.route('/info')
    def handle_home_route(request: Request):
        # fungsi generate_data buat ngegenerate data yang bisa diakses di frontend, lebih dia nambahin route buat GET
        # NOTE: belom tau ini ngerusak threading atau engga
        generate_data(server, '/info/query', content_type='application/json', content=json.dumps(request.query))
        return html_response('info.html')

    @server.route('/content')
    def handle_home_route(request: Request):
        return html_response('content.html')

    @server.route('/about')
    def handle_about_route(request: Request):
        return "This is the about page."
    
    # Set icon
    server.set_icon('assets/favicon.webp')

    # Folder bisa langsung diload semuanya buat method GET
    server.load_static_folder('data')
    server.load_static_folder('scripts')
    server.load_static_folder('assets')

    # Set integrasi database
    server.config["database"] = "sqlite:///test.db"

    server.run()