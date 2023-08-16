from lib.server import *

# Contoh penggunaan
if __name__ == "__main__":
    # Inti penggunaannya mirip flask
    server = Server()
    

    # Returnnya harus dalam bentuk Server_Response, cuman string sama html aja yang dikhususin bisa dihandle tanpa bentuk Server_Response
    @server.route('/', methods=["GET"])
    def handle_home_route(request: Request):
        with open('home.html', 'r') as f:
            content = f.read()
        return Server_Response(content_type='text/html', content=content)

    @server.route('/about', methods=["GET"])
    def handle_about_route(request: Request):
        return "This is the about page."
    
    @server.route('/content', methods=["GET"])
    def handle_home_route(request: Request):
        return html_response('content.html')
    

    # Kalo method di omit, defaultnya dia nambah method GET doang
    @server.route('/home')
    def handle_home_route(request: Request):
        return html_response('home.html')
    
    @server.route('/info')
    def handle_home_route(request: Request):
        return html_response('info.html')


    # Fitur Tambahan: args! bisa ngejadiin route sebagai argumen int atau str
    # NOTE: Kurang di debug. Ga optimizednya minta ampun
    @server.route('/api/dummydata', methods=["PUT"])
    def handle_home_route(request: Request, *args):
        return "Put response with no args"
    
    @server.route('/api/dummydata/<int>', methods=["PUT"])
    def handle_home_route(request: Request, *args):
        return "Put response with one int"
    
    @server.route('/api/dummydata/<str>', methods=["PUT"])
    def handle_home_route(request: Request, *args):
        return "Put response with one string"
    
    @server.route('/api/dummydata/<int>/<int>', methods=["PUT"])
    def handle_home_route(request: Request, *args):
        return "Put response with two ints"
    

    # Semua konten yang dikirim selalu diconvert ke bentuk dictionary
    # NOTE: Yang bisa diterima: Application/json, application/x-www-form-urlencoded, text/plain
    @server.route('/api/dummydata/<int>/uhh/<str>', methods=["PUT"])
    def handle_home_route(request: Request, *args):
        print("ARGS: ", args)
        print("DATA: ", request.contents)
        print("QUERY: ", request.query)
        return "Put response with an int and a str, uhh in between"
    

    # Method bisa dipisah fungsi atau disatuin dan dihandle dari request, terserah gimana yang make frameworknya aja
    @server.route('/api/dummydata/<int>/uhh/<str>', methods=["POST", "DELETE"])
    def handle_home_route(request: Request, *args):
        print("ARGS: ", args)
        print("DATA: ", request.contents)
        print("QUERY: ", request.query)
        return "Post or delete response with an int and a str, uhh in between"


    # Set icon
    server.set_icon('assets/favicon.webp')


    # Folder bisa langsung diload semuanya buat method GET
    server.load_static_folder('data')
    server.load_static_folder('scripts')
    server.load_static_folder('assets')


    # Set integrasi database
    # Bikin sendiri perihal fungsi buat databasenya, kaga begitu gw integrasiin soalnya
    server.config["database"] = "sqlite:///test.db"


    # Gas
    server.run()