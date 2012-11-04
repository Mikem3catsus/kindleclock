import BaseHTTPServer
import ConfigParser
import io
import string
import urllib


# Settings
PORT_NUMBER = 8000


def temperature():
    try:
        URL = "http://www.bom.gov.au/fwo/IDT60901/IDT60901.94970.axf"
        data = urllib.urlopen(URL).read()
        for line in data.split("\n"):
            if line.startswith("0,94970"):
                return line.split(",")[7]
    except:
        pass
    return "???"


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """ Handles GET and HEAD requests.
    """
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        filename = s.path[1:]
        if filename == "":
            filename = "dashboard.html"
        try:
            with open(filename) as f:
                if filename == "dashboard.html":
                    template =  f.read()
                    statichtml = template % {"TEMPERATURE":temperature()}
                    s.wfile.write(statichtml)
                else:
                    s.wfile.write(f.read())
        except:
            pass


if __name__ == '__main__':
    httpd = BaseHTTPServer.HTTPServer(("", PORT_NUMBER), MyHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()