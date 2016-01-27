import unittest
import urllib
import multiprocessing
import server
import time

class ServerTest (unittest.TestCase):
    def setUp(self):
        self.server_process = multiprocessing.Process(target=server.runServer, args=())
        self.server_process.start()
        
    def tearDown(self):
        self.server_process.terminate()
        
    def testMainPage(self):
        handle = urllib.urlopen("http://localhost:8000/")
        text = handle.read()
        self.assertRegexpMatches(text, 'DOCTYPE')
		
    def testSecurity(self):
        """
        urlopen returns a blank string when the requested file doesn't exist. 
        We need to make sure that requests to content outside the content 
        directory is not returned for security reasons.
        """
        bad_filename_list = (
            "server.py", "../server.py", "/python27/bin/python.exe"
        )
        for filename in bad_filename_list:
            handle = urllib.urlopen("http://localhost:8000/" + filename)
            self.assertEqual('', handle.read())
            
if __name__ == '__main__':
    unittest.main()
    exit