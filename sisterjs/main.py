from lib.server import *

# Contoh penggunaan
if __name__ == "__main__":
    # Penggunaannya mirip flask
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


    # Set icon
    server.set_icon('assets/favicon.webp')

    # Folder bisa langsung diload semuanya buat method GET
    server.load_static_folder('data')
    server.load_static_folder('scripts')
    server.load_static_folder('assets')

    # Set integrasi database
    server.config["database"] = "sqlite:///test.db"

    server.run()