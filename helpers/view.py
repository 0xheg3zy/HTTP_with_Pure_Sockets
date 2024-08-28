import os
def render_template(files):
    try:
        html_content = open(os.path.dirname(os.path.abspath(__file__))+"/../templates/index.html" , 'r').read()
        edited_html_content = html_content.replace("edit_me",files)
        return edited_html_content
    except FileNotFoundError:
        print("File Not Found")
    except PermissionError:
        print("Permission denied")
def final_response(file):
    respone_header_download = 'HTTP/1.1 200 OK\nContent-Disposition: attachment; filename="'.encode() + (str(file.split("/")[-1])).encode() + '"\nContent-Type: application/octet-stream\n\n'.encode()
    try:
        current_path = os.getcwd()
        file_content = open(current_path+"/"+file,'rb').read()
        final_return = respone_header_download + file_content
        return final_return
    except PermissionError:
        respone_header_download = 'HTTP/1.1 503 Internal Server Error\n\n'.encode()
        error= "PermissionError".encode()
        return respone_header_download+error
    except Exception as Ex:
        respone_header_download = 'HTTP/1.1 503 Internal Server Error\n\n'.encode()
        return respone_header_download + str(Ex).encode()