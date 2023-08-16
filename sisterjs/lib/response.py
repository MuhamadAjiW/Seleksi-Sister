from lib.util import HTML_ERROR_MESSAGES

# Response Class
class Response():
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
            response = response.encode('utf-8') + self.content
        else:
            response += self.content
            response = response.encode('utf-8')

        return response
    
def html_response(html_page:str):
    with open(html_page, 'r') as f:
        content = f.read()
    return Response(content_type='text/html', content=content)