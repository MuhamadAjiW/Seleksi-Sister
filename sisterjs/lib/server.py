import socket
import threading
import os
import re
from lib.request import Request
from lib.util import HTML_ERROR_MESSAGES
from lib.response import Response
    
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
            
            self.server.run_before_middlewares(request_data)
            response_data = self.server.response(request_data)
            self.server.run_after_middlewares(request_data)

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
        self.before_middlewares = []
        self.after_middlewares = []

        @self.route('/favicon.ico')
        def handle_favicon_route(request):
            return Response(content_type='image/webp', content=self.default_icon)
        
    def load_static_folder(self, folder_path:str):
        # Supported files: .html, .css, .js, .webp, .json, .txt
        # File name must not contain white spaces
        # Will throw an error if not satisfied
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                route_name = os.path.join(root, filename).replace('\\', '/')

                if(route_name.find(' ') != -1):
                    raise Exception(f"File name {route_name} contains spaces. Please remove them.")

                file_type = filename.split('.')[-1]

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

    # Base
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
    
    # Main Functionality
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

                var_comb = ''
                for match in vars:
                    prefix, var_type = match

                    if var_type not in ['str', 'int']:
                        raise Exception(f"var type {var_type} is not a supported type. Please use str or int.")
                    if prefix.find(' ') != -1:
                        raise Exception(f"Route part {prefix} contains spaces. Please remove them.")

                    var_comb += var_type + ','

                if baseroute not in self.routes_vars:
                    self.routes_vars[baseroute] = {}
                
                var_info = vars
                var_dict = {}
                loc = 0
                for vars in var_info:
                    loc += vars[0].count('/')
                    var_dict[loc] = vars[1]

                if var_comb not in self.routes_vars[baseroute]:
                    self.routes_vars[baseroute][var_comb] = {}

                strcomb = ''
                for var in var_dict.keys():
                    strcomb += str(var) + ','

                self.routes_vars[baseroute][var_comb][strcomb] = var_dict

    
            if route not in self.routes:
                self.routes[route] = {}
            
            for method in methods:
                self.routes[route][method] = func

            def decorated_func(request: Request, *args):
                return func(request, *args)
            return decorated_func
        
        return decorator

    def response(self, request_data):
        # try:
            request = Request(request_data)
            uses_vars = False
            pref = ''

            route_funcs = self.routes.get(request.addr, {})

            if route_funcs == {}:

                # Possible var
                for var_info in self.routes_vars:
                    if request.addr.startswith(var_info):
                        route_funcs = self.routes.get(var_info, {})
                        uses_vars = True
                        pref = var_info
                        break
                
                if not uses_vars:
                    print("ERROR: NOT FOUND") # LOG
                    if(self.routes.get(404)):
                        return self.routes.get(404)(request).generate(self.server_name, keep_connection=False)
                    
                    return Response(status_code=404, content_type='text/plain', content='404 Not Found').generate(self.server_name, keep_connection=False)
        


            route_func = route_funcs.get(request.type)

            # Vars detection
            if uses_vars:
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
                    var_idxs = self.routes_vars[pref][var_comb]

                    for entries in var_idxs:

                        entrystr = entries[:-1]
                        entry = entrystr.split(',')

                        for i in range(len(entry)):
                            entry[i] = int(entry[i])

                        if(len(vals) < max(entry) + 1):
                            continue
                        else:
                            args = list(entry)
                            for i in range(startidx, len(vals)):

                                if i in entry:
                                    if entry_types[entry.index(i)] == 'int':
                                        try:
                                            intval = int(vals[i])
                                            compstring += '/' + str(intval)
                                            args[entry.index(i)] = intval
                                            success = True
                                        except:
                                            success = False
                                            break
                                    else:
                                        if vals[i].find(' ') != -1:
                                            success = False
                                            break
                                        else:
                                            compstring += '/' + vals[i]
                                            args[entry.index(i)] = vals[i]
                                else:
                                    compstring += '/' + vals[i]
                                
                                if not request.addr.startswith(compstring):
                                    success = False
                                    break

                            if success and compstring == request.addr:
                                success = True
                                break

                            if not success:
                                compstring = pref
                
                    if success:
                        newpath = ''
                        for i in range(1, len(vals)):
                            if i not in entry:
                                newpath += '/' + vals[i]
                            else:
                                newpath += f'/<{entry_types[entry.index(i)]}>'
                        
                        route_funcs = self.routes.get(newpath, {})
                        route_func = route_funcs.get(request.type)

                        if route_func:
                            response = route_func(request, *args)

                            if type(response) == str:
                                response = Response(content=response)

                            return response.generate(self.server_name, keep_connection=False)

                    compstring = pref
                    
                print("ERROR: NOT FOUND") # LOG
                if(self.routes.get(404)):
                    return self.routes.get(404)(request).generate(self.server_name, keep_connection=False)
                
                return Response(status_code=404, content_type='text/plain', content='404 Not Found').generate(self.server_name, keep_connection=False)


            # Without vars
            elif route_func:
                response = route_func(request)

                if type(response) == str:
                    response = Response(content=response)

                return response.generate(self.server_name, keep_connection=False)

            # Found but no method
            print("ERROR: NOT ALLOWED") # LOG
            if(self.routes.get(405)):
                return self.routes.get(405)(request).generate(self.server_name, keep_connection=False)
            return Response(status_code=405, content_type='text/plain', content='405 Method Not Allowed').generate(self.server_name, keep_connection=False)

        # General failure
        # except Exception as e:
        #     print("ERROR: INTERNAL ERROR") # LOG
        #     print(e.args)
        #     print(e.with_traceback) # LOG
        #     if(self.routes.get(500)):
        #         return self.routes.get(500)(request).generate(self.server_name, keep_connection=False)
            
        #     return Response(status_code=500, content_type='text/plain', content='500 Internal Error').generate(self.server_name, keep_connection=False)
        
    # Tertiary functionality
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
            return Response(content_type='image/webp', content=self.default_icon)

    # Middlewares
    def before_request(self):
        def decorator(func):
            self.before_middlewares.append(func)
            def decorated_func(request, *args):
                response = func(request, *args)
                return response
            return decorated_func
        return decorator
    
    def after_request(self):
        def decorator(func):
            self.after_middlewares.append(func)
            def decorated_func(request, *args):
                response = func(request, *args)
                return response
            return decorated_func
        return decorator

    def run_before_middlewares(self, request):
        for middleware in self.before_middlewares:
            middleware(request)
    
    def run_after_middlewares(self, request):
        for middleware in self.after_middlewares:
            middleware(request)


# Global Functions
def generate_static_response(server: Server, route_name:str, content_type:str='*/*', read_type='r'):
    @server.route('/' + route_name)
    def handle_file_route(request):
        with open(route_name, read_type) as f:
            content = f.read()
        return Response(content_type=content_type, content=content)
    