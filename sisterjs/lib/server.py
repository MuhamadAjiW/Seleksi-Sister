# Disclaimer dulu

# kalo ini frameworknya rada aneh maap banget
# Gw kaga ada pengalaman web samsek
# Asal jalan doang kaga tau struktur
# Maapin

import socket
import threading
import os
import json
import re
import sqlite3
from constants import *

# Request Class
class Request():
    def __init__(self, reqstr:str=''):
        # print("Received data:") # LOG
        # print(reqstr) # LOG
        
        reqstr = reqstr
        area = reqstr.split('\r\n\r\n')
        httplines = area[0].split('\r\n')
        request_line = httplines[0].split(' ')
        addr = request_line[1]
        addr_cnt = addr.split('?')

        self.type: str = request_line[0]
        self.addr: str = addr_cnt[0]
        self.query: dict = {}
        self.contents: dict = {}
        self.acc_type: str = ''

        print("Request addr: ", self.addr) # LOG
        print("Request type: ", self.type) # LOG

        if(self.type == 'GET'):
            for line in httplines:
                if(line.find('Accept:') != -1):
                    self.acc_type: str = line.split(': ')[1]
                    print("Request accepts: ", end=' ') # LOG
                    print(self.acc_type) # LOG

        lastln = httplines[len(httplines) - 1].split(': ')
        if(lastln[0] == "Content-Type"):
            self.content_type: str = lastln[1]
            print("Request has content: ", end=' ') # LOG
            print(self.content_type)

            if(self.content_type == 'application/x-www-form-urlencoded'):
                self.contents = extract_wwwquery(area[1])
            elif(self.content_type == 'text/plain'):
                self.contents = extract_plaintext(area[1])
            elif(self.content_type == 'application/json'):
                self.contents = extract_json(area[1])

            print("Request contents: ") # LOG
            print(self.contents) # LOG

        if(len(addr_cnt) > 1):
            self.query = extract_wwwquery(addr_cnt[1])

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
f"HTTP/1.1 {self.status_code} {HTML_ERROR_MESSAGES[self.status_code]}\r\n"
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

        print("Worker Thread Closed Successfully.\n\n") # LOG
    
# Main Server Class
class Server():
    def __init__(self, port:int=10000, addr:str='127.0.0.1', limit:int=5):
        self.default_icon = ''.encode('utf-8')
        self.server_name = "pyster/0.1.0"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.addr = addr
        self.socket.bind((addr, self.port))
        self.socket.listen(limit)
        self.running = False
        self.routes = {}
        self.routes_vars = {}
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
                
    def run(self):
        print(f"Server running on {self.addr}:{self.port}\n\n")
        self.running = True
        while self.running:
            client_socket, client_address = self.socket.accept()
            handler = Server_Handler(client_socket, client_address, self)
            handler.start()

    def stop(self):
        self.running = False
        self.socket.close()
    
    def route(self, route, methods:list=['GET']):
        def decorator(func):
            if methods == None:
                raise Exception("Methods cannot be None.")
            if(route.find(' ') != -1):
                raise Exception(f"Route name {route} contains spaces. Please remove them.")
            
            pattern = r'([^<]*)<([^<]+)>'
            vars = re.findall(pattern, route)
            if len(vars) > 0:
                baseroute = vars[0][0][:-1]

                # print("Route contains parameters.") # LOG                
                # print(vars)
                # print(baseroute)
                var_comb = ''
                for match in vars:
                    prefix, var_type = match

                    if var_type not in ['str', 'int']:
                        raise Exception(f"var type {var_type} is not a supported type. Please use str or int.")
                    if prefix.find(' ') != -1:
                        raise Exception(f"Route part {prefix} contains spaces. Please remove them.")

                    var_comb += var_type + ','
                    # print("Prefix:", prefix)
                    # print("Variable Name:", var_name)

                if baseroute not in self.routes_vars:
                    self.routes_vars[baseroute] = {}
                
                # print(var_comb)
                var_info = vars
                var_dict = {}
                loc = 0
                for vars in var_info:
                    loc += vars[0].count('/')
                    var_dict[loc] = vars[1]
                # print(var_info)
                # print(var_dict)

                if var_comb not in self.routes_vars[baseroute]:
                    self.routes_vars[baseroute][var_comb] = {}

                strcomb = ''
                for var in var_dict.keys():
                    strcomb += str(var) + ','
                # print(strcomb)

                self.routes_vars[baseroute][var_comb][strcomb] = var_dict
                # print(baseroute)

    
            if route not in self.routes:
                self.routes[route] = {}
            
            print("Adding method for route: ", route) # LOG
            for method in methods:
                print(method) # LOG
                self.routes[route][method] = func

            def decorated_func(request: Request, *args):
                return func(request, *args)
            return decorated_func
        
        return decorator
            
    def error_page(self, error_code):
        def decorator(func):
            self.routes[error_code] = func
            def decorated_func(request, *args):
                return func(request, *args)
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
            uses_vars = False
            pref = ''

            route_funcs = self.routes.get(request.addr, {})

            if route_funcs == {}:

                # Possible var
                print(self.routes_vars)
                for var_info in self.routes_vars:
                    print(var_info)
                    print(request.addr)
                    if request.addr.startswith(var_info):
                        route_funcs = self.routes.get(var_info, {})
                        uses_vars = True
                        pref = var_info
                        break
                
                if not uses_vars:
                    print("ERROR: NOT FOUND") # LOG
                    if(self.routes.get(404)):
                        return self.routes.get(404)(request).generate(self.server_name, keep_connection=False)
                    
                    return Server_Response(status_code=404, content_type='text/plain', content='404 Not Found').generate(self.server_name, keep_connection=False)
        


            route_func = route_funcs.get(request.type)

            # Vars detection
            if uses_vars:
                print("ROUTE MIGHT USE VARS")
                args = None
                entry = None
                entry_types = None
                vals = request.addr.split('/')
                compstring = pref
                startidx = compstring.count('/') + 1
                for var_comb in self.routes_vars[pref]:

                    success = False
                    varstring = var_comb[:-1]
                    entry_types = varstring.split(',')
                    print(entry_types)
                    var_idxs = self.routes_vars[pref][var_comb]

                    print(var_idxs)
                    for entries in var_idxs:
                        print("Examining: ", entries)

                        entrystr = entries[:-1]
                        entry = entrystr.split(',')
                        print("entry: ", entry)

                        for i in range(len(entry)):
                            entry[i] = int(entry[i])

                        print("now entry: ", entry)

                        if(len(vals) < max(entry) + 1):
                            print("Not enough entries")
                        else:
                            args = list(entry)
                            for i in range(startidx, len(vals)):
                                print("VALS: ", vals[i])

                                print("entry for now:", entry)
                                if i in entry:
                                    print("Examining value: ", vals[i])
                                    if entry_types[entry.index(i)] == 'int':
                                        try:
                                            print("Should be int")
                                            intval = int(vals[i])
                                            compstring += '/' + str(intval)
                                            args[args.index(i)] = intval
                                            print("passed")
                                            success = True
                                        except:
                                            success = False
                                            break
                                    else:
                                        print("Should be str")
                                        compstring += '/' + vals[i]
                                        args[args.index(i)] = intval
                                        print("passed")
                                else:
                                    compstring += '/' + vals[i]
                                
                                print(compstring)
                                if not request.addr.startswith(compstring):
                                    success = False
                                    break

                            print("result for:", entry)
                            print(compstring)
                            if success and compstring == request.addr:
                                print("SUCCESS WITH ENTRY: ", entry)
                                success = True
                                break

                            if not success:
                                compstring = pref

                    print("Success: ", success)
                    if success:
                        break                        
                
                if success:
                    newpath = ''
                    print("entry: ", entry)
                    print("entry_types: ", entry_types)
                    for i in range(1, len(vals)):
                        if i not in entry:
                            newpath += '/' + vals[i]
                        else:
                            newpath += f'/<{entry_types[entry.index(i)]}>'
                        print(newpath)
                    
                    print("finalpath: ",newpath)

                    route_funcs = self.routes.get(newpath, {})
                    route_func = route_funcs.get(request.type)

                    if route_func:
                        print("ROUTE FOUND WITH VARS") # LOG

                        response = route_func(request, *args)

                        if type(response) == str:
                            response = Server_Response(content=response)

                        return response.generate(self.server_name, keep_connection=False)

            # Without vars
            elif route_func:
                print("ROUTE FOUND") # LOG
                response = route_func(request)

                if type(response) == str:
                    response = Server_Response(content=response)

                return response.generate(self.server_name, keep_connection=False)

            # Found but no method
            print("ERROR: NOT ALLOWED") # LOG
            if(self.routes.get(405)):
                return self.routes.get(405)(request).generate(self.server_name, keep_connection=False)
            return Server_Response(status_code=405, content_type='text/plain', content='405 Method Not Allowed').generate(self.server_name, keep_connection=False)

        # General failure
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

def extract_wwwquery(query:str):
    query_dict = {}
    query_cnt = query.split('&')
    for query in query_cnt:
        query_pair = query.split('=')
        query_dict[query_pair[0]] = query_pair[1]
    return query_dict

def extract_plaintext(query:str):
    query_dict = {}
    query["content"] = query
    return query_dict

def extract_json(query:str):
    query_dict = json.loads(query)
    return query_dict

# Main, contoh penggunaan
if __name__ == "__main__":
    server = Server()
    
    @server.route('/', methods=["GET"])
    def handle_home_route(request: Request, *args):
        return html_response('home.html')
    
    @server.route('/home')
    def handle_home_route(request: Request, *args):
        return html_response('home.html')
    
    @server.route('/info')
    def handle_home_route(request: Request, *args):
        return html_response('info.html')

    @server.route('/content')
    def handle_home_route(request: Request, *args):
        return html_response('content.html')

    @server.route('/about')
    def handle_about_route(request: Request, *args):
        return "This is the about page."

    server.set_icon('assets/favicon.webp')

    server.load_static_folder('data')
    server.load_static_folder('scripts')
    server.load_static_folder('assets')

    server.config["database"] = "sqlite:///test.db"

    @server.route('/api/dummydata', methods=["POST"])
    def handle_home_route(request: Request, *args):
        return html_response('home.html')
    
    @server.route('/api/dummydata', methods=["PUT"])
    def handle_home_route(request: Request, *args):
        print("Put response, unwanted")
        return html_response('home.html')
    
    @server.route('/api/dummydata/<int>/<int>', methods=["PUT"])
    def handle_home_route(request: Request, *args):
        print("ARGS: ", args)
        return html_response('home.html')
    
    @server.route('/api/dummydata/<int>/uhh/<int>', methods=["PUT"])
    def handle_home_route(request: Request, *args):
        print("ARGS: ", args)
        print(args[0])
        print(args[1])
        return html_response('home.html')
    
    @server.route('/api/dummydata/<int>', methods=["PUT"])
    def handle_home_route(request: Request, *args):
        print("ARGS: ", args)
        print(args[0])
        return html_response('home.html')
    
    @server.route('/api/dummydata', methods=["DELETE"])
    def handle_home_route(request: Request, *args):
        return html_response('home.html')

    # print(server.routes_vars["/api/dummydata"])
    server.run()