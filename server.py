import socket as s
from os import *
from view import *
from uri_handler import *
from sys import *
from socket import *
so=s.socket(s.AF_INET,s.SOCK_STREAM)
so.bind(('127.0.0.1',8000))
so.listen(1)
correct_respone_header = "HTTP/1.1 200 OK\n\n".encode()
correct_status_code="200"
error_respone_header="HTTP/1.1 503 Internal Server Error\n\n".encode()
correct_status_code="503"
while True:
	try:
		conn,addr=so.accept()
		d=conn.recv(1024)
		if len(d)==0:
			conn.close()
			continue
		else:
			uri_index = (d.decode().split("\n")[0].split(" ")[1])
			uri_path = handler(uri_index)
			content_type = uri_path.split(" ")[0]
			if content_type == "BaSeInDex":
				html_body = render_template(uri_path.replace("BaSeInDex ",""))
				conn.send(correct_respone_header + html_body.encode())
				conn.close()
				print("200")
			elif content_type == "File":
				file_name=uri_path.replace("File ", "")
				if "HTTP/1.1 503 Internal Server Error".encode() in final_response(file_name):
					status_code="503"
					conn.send(final_response(file_name))
					conn.close()
				else:
					status_code="200"
					conn.sendall(final_response(file_name))
					conn.close()
				print(status_code)
			elif content_type == "Directory":
				if uri_path.split(" ")[1] == "Permission_denied":
					html_body="PermissionDenied"
					status_code="503"
					conn.send(error_respone_header + html_body.encode())
					conn.close()
				else:
					html_body = render_template(uri_path.replace("Directory ", ""))
					conn.send(correct_respone_header + html_body.encode())
					status_code="200"
					conn.close()
				print(status_code)
			elif content_type == "N0tF0uNd":
				respone_header = "HTTP/1.1 404 NotFound\n\n".encode()
				html_body = render_template(uri_path.replace("N0tF0uNd ", ""))
				conn.send(respone_header + html_body.encode())
				conn.close()
				print("404")
			else:
				html_body = render_template(uri_path.replace("N0TSenDed ", ""))
				conn.send(error_respone_header + html_body.encode())
				conn.close()
				print("503")
			files_array.clear()
	except KeyboardInterrupt:
		print("^c is recieved , exiting ...")
		so.close()
		exit()
	except Exception as Ex:
		print("Exception : >>>>>>>>" + str(Ex))
		so.close()
		continue