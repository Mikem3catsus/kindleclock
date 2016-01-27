import BaseHTTPServer
import sources
import tools
import logging
import os
import re
#logging.basicConfig(level=logging.INFO)

# Settings
PORT_NUMBER = 8000
SOURCES = {
    "TEMPERATURE": sources.temperature,
    "FORECAST": sources.forecast,
    "AGENDA": sources.agenda,
    "UNREADGMAIL": sources.unreadgmail,
}


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """ Handles GET and HEAD requests.
    """
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", tools._content_type(tools._filename(s)))
        s.end_headers()
        logging.info("completed do_HEAD")
        
    def do_GET(s):
        filename = tools._filename(s)

        # Fire off some headers with the content type
        s.send_response(200)
        s.send_header("Content-type", tools._content_type(filename))
        s.end_headers()

        filename = s.cleanup_filename(filename)
        
        if not os.path.exists(filename):
            return
            
        with open(filename, 'rb') as f:
            if filename == "dashboard.html":
                template =  f.read()
                tempdict = {}
                for k,func in SOURCES.items():
                    tempdict[k] = func()
                statichtml = template % tempdict
                s.wfile.write(statichtml)
            else:
                s.wfile.write(f.read())

        logging.info("completed do_GET")
        
    def cleanup_filename(self, filename):
        """
        fix the filename up so that it  has defaults and is secure, only using files in the 'content' directory.
        It does not support hierarchy within the content directory (for simplicity and safety).
        """
        if filename == "":
            filename = "dashboard.html"
        if filename == "favicon.ico":
            return
        
        filename = re.sub('[^\w\d\.\_\-]','', filename)
        filename = os.path.join('content', filename)
        return filename
        
    def log_message(self, format, *args):
        return

def runServer():
    httpd = BaseHTTPServer.HTTPServer(("", PORT_NUMBER), MyHandler)
    logging.info("starting server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    
if __name__ == '__main__':
    runServer()
    exit
    