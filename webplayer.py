import ure, time, socket

DEBUG = False

def _debug(*args):
    if DEBUG:
        print(*args)


class WebPlayer:
    """ TODO
    """
    
    def __init__(self, mp3Player):
        self.mp3Player = mp3Player
        self.html_file = "index.html"
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(False) 
        self.sock.bind(addr)
        self.sock.listen(4)
        _debug('listening on', addr)

    def do(self):
        """ called regularly from the main loop
        """
        try:
            cl, addr = self.sock.accept()
            #cl.setblocking(False) #TODO is it neccesarry?
            _debug('client connected from', addr)
        except OSError:
            #no connection
            return
        
        try:
            request = None
            for i in range(30): #max X Iterationen
                try:
                    _debug("trying to receive data...")
                    request = str(cl.recv(1024))
                    _debug("REQUEST: ", request)
                    break
                except OSError:
                    #not ready to recv yet
                    time.sleep(0.1)
                    continue
            else:
                _debug("Error: This took too long!!")
                cl.close()
                return
            obj = ure.search("GET (.*?) HTTP\/1\.1", request)
            if obj:
                _debug(obj.group(1))
                path, parameters = self.parseURL(obj.group(1))
                if path.startswith("/folder"):
                    folder=parameters.get("folder",1)
                    _debug(folder, repr(folder))
                    self.mp3Player.play_folder(int(folder))
                elif path.startswith("/play"):
                    track=parameters.get("track",1)
                    self.mp3Player.play_track(int(track))
                elif path.startswith("/next"):
                    self.mp3Player.next()
                elif path.startswith("/prev"):
                    self.mp3Player.previous()
                elif path.startswith("/resume"):
                    self.mp3Player.resume()
                elif path.startswith("/pause"):
                    self.mp3Player.pause()
                elif path.startswith("/volume"):
                    level=int(parameters.get("level",15))
                    self.mp3Player.set_volume(level)
                elif path.startswith("/halt"):
                    cl.close()
                    raise SystemExit('Stop program')
                else:
                    _debug("UNREGISTERED ACTION\r\nPATH: %s\r\nPARAMETERS: %s" % (path, parameters))
            try:
                self.sendResponse(cl)
            except OSError as e:
                _debug(e)
        finally:
            cl.close()
            _debug("connection closed")
     
    def parseURL(self, url):
        #PARSE THE URL AND RETURN THE PATH AND GET PARAMETERS
        parameters = {}
        path = ure.search("(.*?)(\?|$)", url) 
        while True:
            vars = ure.search("(([a-z0-9]+)=([a-z0-9.]*))&?", url)
            if vars:
                parameters[vars.group(2)] = vars.group(3)
                url = url.replace(vars.group(0), '')
            else:
                break
        return path.group(1), parameters

        
    def sendResponse(self, cl):
        header = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
        self._sendResponseLine(cl, header)
        f = open(self.html_file)
        for line in f:
            self._sendResponseLine(cl, line)
        _debug("finished sending")
            
    def _sendResponseLine(self, cl, line):
        for i in range(30): #try max 30 times
            sent = cl.write(line)
            if sent == None:
                #could not write, try again
                time.sleep(0.1)
                _debug("trying to send again")
                continue
            else:
                return
        
