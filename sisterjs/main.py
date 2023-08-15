from api.server import *

if __name__ == "__main__":
    server = Server()

    @server.route('/')
    def handle_home_route():
        return html_response('test.html')

    @server.route('/about')
    def handle_about_route():
        return "This is the about page."
    
    @server.error_page(400)
    def handle_404_error():
        return html_response('error.html')
    
    server.set_icon('assets/favicon.webp')
    server.load_static_folder('data')
    server.load_static_folder('scripts')
    server.load_static_folder('assets')

    server.run()