import base64
import re
import urllib
import urllib2
import xml.dom.minidom


def unreadgmail():
    try:
        auth = open("gmailauth.txt").read()
        URL = 'https://gmail.google.com/gmail/feed/atom'
        req = urllib2.Request(URL)
        req.add_header('Authorization', 'Basic %s' % auth)
        dom = xml.dom.minidom.parse(urllib2.urlopen(req))
        count = int(dom.getElementsByTagName("fullcount")[0].lastChild.toxml())
        if count == 0:
            return "No unread emails"
        elif count == 1:
            return "1 new email"
        else:
            return "{0} new emails".format(count)
    except:
        pass
    return "???"


def agenda():
    """ Returns events from a google calendar URL. For instance you could use a
        private one like:
        
        https://www.google.com/calendar/feeds/[email address]/private-[stuff]/basic?[options]
        
        The url is stored in calxmlurl.txt in the same folder as sources.py.

        The options are whatever suits, I use:

        orderby=starttime&sortorder=ascending&singleevents=true&futureevents=true&max-results=5

        See the following for hints on options:
         * https://developers.google.com/google-apps/calendar/v2/reference#Parameters
         * https://developers.google.com/gdata/docs/2.0/reference#Queries
    """

    try:
        results = ""
        URL = open("calxmlurl.txt").read()
        dom = xml.dom.minidom.parse(urllib.urlopen(URL))
        entries = dom.getElementsByTagName("entry")
        for e in dom.getElementsByTagName("entry"):
            event = e.getElementsByTagName("title")[0].lastChild.toxml()\
                        .encode('ascii','ignore')
            times = e.getElementsByTagName("summary")[0].lastChild.toxml()\
                        .encode('ascii','ignore').split("\n")[0]
            times = re.findall(r'.*?([0-9]{2}:[0-9]{2}).*?', times)
            displaytime = "All day"
            if len(times) == 1:
                displaytime = times[0]
            elif len(times) == 2:
                displaytime = times[0] + "-" + times[1]
            results += event + " - <em>" + displaytime + "</em> " + "<br />"
        return results
    except:
        pass
    return "???"


def forecast():
    try:
        URL = "ftp://ftp2.bom.gov.au/anon/gen/fwo/IDA00007.dat"
        data = urllib.urlopen(URL).read()
        temp = ""
        for line in data.split("\n"):
            if line.startswith("094029"):
                if (line.split("#")[6] != ""):
                    temp = "Min: " + line.split("#")[6] + ", "
                if (line.split("#")[7] != ""):
                    temp += "Max: " + line.split("#")[7]
        if temp != "":
            temp += "<br />"
        for line in data.split("\n"):
            if line.startswith("094029"):
                return temp + line.split("#")[22]
    except:
        pass
    return "???"


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