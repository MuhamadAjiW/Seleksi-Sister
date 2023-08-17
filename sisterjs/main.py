from lib.server import *
from lib.response import *
from lib.database import *
import sqlite3

# Disclaimer dulu

# Kalo ini frameworknya rada aneh maap banget
# Gw kaga ada pengalaman web samsek
# Asal jalan doang, kaga tau struktur
# Enjoy kode tai gw

# Contoh penggunaan
if __name__ == "__main__":
    # Inti penggunaannya mirip flask
    server = Server(10000)
    

    # Returnnya harus dalam bentuk Response, cuman string sama html aja yang dikhususin bisa dihandle tanpa bentuk Server_Response
    @server.route('/', methods=["GET"])
    def handle_home_route(request: Request):
        with open('home.html', 'r') as f:
            content = f.read()
        return Response(content_type='text/html', content=content)

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


    # Fitur Tambahan: 
    # args! bisa ngejadiin route sebagai argumen int atau str (str gak boleh make '/' atau ' ')
    # NOTE: Kurang di debug. Ga optimizednya minta ampun, kemungkinan besar banget masi bikin bug
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
        print("ACCEPT: ", request.acc_type)
        print("DATA: ", request.contents)
        print("QUERY: ", request.query)
        return "Put response with an int and a str, uhh in between"
    

    # Method bisa dipisah fungsi atau disatuin dan dihandle dari request, terserah gimana yang make frameworknya aja
    @server.route('/api/dummydata/<int>/uhh/<str>', methods=["POST", "DELETE"])
    def handle_home_route(request: Request, *args):
        print("ARGS: ", args)
        print("ACCEPT: ", request.acc_type)
        print("DATA: ", request.contents)
        print("QUERY: ", request.query)
        return "Post or delete response with an int and a str, uhh in between"


    # Middleware! ada 2 middle ware, before request sama after request (niru flask banget emang ini ehe)
    @server.before_request()
    def handle_before_request(request: Request):
        print("Middleware before request")

    @server.after_request()
    def handle_before_request(request: Request):
        print("Middleware after request")


    # Set icon
    server.set_icon('assets/favicon.webp')


    # Folder bisa langsung diload semuanya dan rekursif ke dalem buat method GET
    server.load_static_folder('scripts')
    server.load_static_folder('assets')


    # Set integrasi database
    # Bikin sendiri perihal fungsi buat databasenya, kaga gw integrasiin
    # Tapi kan udah bisa terima data dari request yak, jadi cukup memenuhi spek harusnya
    server.config["database"]: str = "data/dummy.db"
    connection = connect_db(server.config["database"])


    # Oke ini buat API web dummynya
    init_db(connection)
    close_db(connection)

    @server.route('/api/info', methods=["GET"])
    def handle_home_route(request: Request, *args):
        index = int(request.query.get('index'))
        if index is not None:
            try:
                index = int(index)
                conn = connect_db(server.config["database"])
                cursor = conn.cursor()
                cursor = cursor.execute('SELECT * FROM istri LIMIT 1 OFFSET ?', (index,))
                data = cursor.fetchone()
                close_db(conn)

                if data:
                    return json_response({'name': data[1], 'desc': data[2]})

                return json_response({'error': 'Data not found'}, 404)
            
            except Exception as e:
                return json_response({'error': 'An error occured'}, 500)
            
        else:
            return json_response({'error': 'No index provided'}, 400)
        
    @server.route('/api/infoall', methods=["GET"])
    def handle_home_route(request: Request, *args):
        try:
            conn = connect_db(server.config["database"])
            cursor = conn.cursor()
            cursor = cursor.execute('SELECT * FROM istri')
            data = cursor.fetchall()
            close_db(conn)

            if data:
                result = []
                for row in data:
                    result.append({'name': row[1], 'desc': row[2]})
                return json_response(result)

            return json_response({'error': 'Data not found'}, 404)
        
        except Exception as e:
            return json_response("{'error': 'An error occured'}}", 500)
    
    @server.route('/api/info', methods=["POST"])
    def handle_home_route(request: Request, *args):
        try:
            name = request.contents['name']
            desc = request.contents['desc']
            if name and desc:
                conn = connect_db(server.config["database"])
                cursor = conn.cursor()
                cursor = cursor.execute('INSERT INTO istri (name, desc) VALUES (?, ?)', (name, desc))
                close_db(conn)
                return json_response({'message': 'Addition success'}, 200)

            return json_response({'error': 'Data is invalid'}, 400)
        
        except Exception as e:
            return json_response("{'error': 'An error occured'}}", 500)

    @server.route('/api/info', methods=["PUT"])
    def handle_home_route(request: Request, *args):
        index = int(request.query.get('index'))
        name = request.contents['name']
        desc = request.contents['desc']
        try:
            if name and desc:
                conn = connect_db(server.config["database"])
                cursor = conn.cursor()
                cursor = cursor.execute('UPDATE istri SET name = ?, desc = ? WHERE id = (SELECT id FROM istri LIMIT 1 OFFSET ?)', (name, desc, index))
                print("Editing entry")
                close_db(conn)

                if cursor.rowcount > 0:
                    return json_response({'message': 'Edition success'}, 200)

            return json_response({'error': 'Data is invalid'}, 400)
        
        except Exception as e:
            return json_response("{'error': 'An error occured'}}", 500)

    @server.route('/api/info', methods=["DELETE"])
    def handle_home_route(request: Request, *args):
        index = int(request.query.get('index'))
        try:
            conn = connect_db(server.config["database"])
            cursor = conn.cursor()
            cursor = cursor.execute('DELETE FROM istri WHERE id = (SELECT id FROM istri LIMIT 1 OFFSET ?)', (index,))
            close_db(conn)

            if cursor.rowcount > 0:
                return json_response({'message': 'Deletion success'}, 200)

            return json_response({'error': 'Data not found'}, 404)
        
        except Exception as e:
            return json_response("{'error': 'An error occured'}}", 500)


    # Gas
    server.run()

    #closingan
    server.stop()
    close_db(server.config["database"])