from lib.util import extract_wwwquery, extract_plaintext, extract_json

# Request Class
class Request():
    def __init__(self, reqstr:str=''):
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
        self.content_length: int = 0

        for line in httplines:
            accloc = line.find('Accept:')
            contentloc = line.find('Content-Type:')
            lengthloc = line.find('Content-Length:')

            if(accloc != -1):
                self.acc_type: str = line.split(': ')[1]
            
            if(contentloc != -1):
                self.content_type: str = line.split(': ')[1]
                if(self.content_type == 'application/x-www-form-urlencoded'):
                    self.contents = extract_wwwquery(area[1])
                elif(self.content_type == 'text/plain'):
                    self.contents = extract_plaintext(area[1])
                elif(self.content_type == 'application/json'):
                    self.contents = extract_json(area[1])
            
            if(lengthloc != -1):
                self.content_length: int = int(line.split(': ')[1])

        if(len(addr_cnt) > 1):
            self.query = extract_wwwquery(addr_cnt[1])