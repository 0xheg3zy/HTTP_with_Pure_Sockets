#!/usr/bin/env python3
import socket as s
from os import *
from sys import *
from socket import *
import threading
from helpers.view import render_template,final_response
from helpers.uri_handler import handler,files_array
so=s.socket(s.AF_INET,s.SOCK_STREAM)
so.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
so.bind(('127.0.0.1',8000))
so.listen(1)
correct_respone_header = "HTTP/1.1 200 OK\n\n".encode()
correct_status_code="200"
error_respone_header="HTTP/1.1 503 Internal Server Error\n\n".encode()
correct_status_code="503"

def main_code(conn,addr):
	try:
		d=conn.recv(1024)
		if len(d)==0:
			conn.close()
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
	except Exception as EXP:
		print(f"[ERROR] {EXP}")
	finally:
		conn.close()

while True:
	try:
		conn,addr=so.accept()
		client_thread = threading.Thread(target=main_code, args=(conn, addr))
		client_thread.start()
	except KeyboardInterrupt:
		print("^c is recieved , exiting ...")
		so.close()
		exit()