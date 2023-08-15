from api.server import *

if __name__ == "__main__":
    server = Server()
    
    @server.route('/')
    def handle_home_route(**kwargs):
        return html_response('home.html')
    
    @server.route('/home')
    def handle_home_route(**kwargs):
        return html_response('home.html')
    
    @server.route('/info')
    def handle_home_route(**kwargs):
        generate_query(server, '/info/query', content_type='application/json', content=kwargs_to_json(**kwargs.get('query')))
        return html_response('info.html')

    @server.route('/content')
    def handle_home_route(**kwargs):
        return html_response('content.html')

    @server.route('/about')
    def handle_about_route(**kwargs):
        return "This is the about page."
    
        
    server.set_icon('assets/favicon.webp')
    server.load_static_folder('data')
    server.load_static_folder('scripts')
    server.load_static_folder('assets')

    server.run()