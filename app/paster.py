import paste.httpserver
import wsgi

if __name__ == '__main__':
	paste.httpserver.serve(wsgi.application, host='127.0.0.1', port='8888')
