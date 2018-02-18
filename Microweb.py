import re
import traceback
    
class wsgiapp:
    """The most beatiful pragmatic micro web framwork.
        
    How to use:
        
        class application(wsgiapp):
            urls = [
                ("/(.*)", "index"),
            ]
            def GET_hello(self, name):
                self.header("Content-Type", "text/plain")
                return "Hello, %s!" % name
    """
        
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
        self.status = "200 OK"
        self._headers = []
            
    def header(self, name, value):
        self._headers.append((name, value))
            
    def __iter__(self):
        try:
            x = self.delegate()
            self.start(self.status, self._headers)
        except:
            headers = [("Content-Type", "text/plain")]
            self.start("500 Internal Error", headers)
            x = "Internal Error:\n\n" + traceback.format_exc()
            
        # return value can be a string or a list. we should be able to 
        # return an iter in both the cases.
        if isinstance(x, str):
            return iter([x])
        else:
            return iter(x)

    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']
            
        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups() 
                funcname = method.upper() + "_" + name
                func = getattr(self, funcname)
                return func(*args)
                    
        return self.notfound()