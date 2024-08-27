from os import *
from time import *
files_array =[]
def type(file_or_dir):
    file_or_dir = "./"+file_or_dir
    if path.exists(file_or_dir):
        if path.isfile(file_or_dir):
            return "File"
        elif path.isdir(file_or_dir):
            return "Directory"
        else:
            return "Unknown"
    else:
        return "N0tF0uNd"
def handler(uri_index):
    print(" time : [\"" + ctime() + "\"] request : \"" +uri_index +"\" ",end="")
    file_or_dir = uri_index
    if uri_index == '/':
        for file_or_dir in listdir("."):
            files_array.append("		<p><span>> </span><a href=\""+file_or_dir+"\">"+file_or_dir+"</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+type(file_or_dir) + "</p>")
        returned_values = "\n".join(files_array)
        return "BaSeInDex "+returned_values
    elif type(uri_index) == "File" and ".." not in uri_index:
            files_array.append("		<p><span>> </span><a href=\""+uri_index+"/"+file_or_dir+"\">"+file_or_dir.split("/")[-1]+"</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;File</p>")
            return "File ." + uri_index
    elif type(uri_index) == "Directory":
        try:
            for file_or_dir in listdir("."+uri_index+"/"):
                files_array.append("		<p><span>> </span><a href=\""+uri_index+"/"+file_or_dir+"\">"+file_or_dir+"</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+type("./"+uri_index+"/"+file_or_dir) + "</p>")
            returned_values = "\n".join(files_array)
            return "Directory " + returned_values
        except PermissionError:
            return "Directory Permission_denied"
    elif type(uri_index) == "N0tF0uNd":
        files_array.append("		<p><center><p>404 Not Found</p></center>nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p>")
        returned_values = "\n".join(files_array)
        return "N0tF0uNd " + returned_values
    else:
        files_array.append("		<p><center><p>Can't Be Sended</p></center>nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p>")
        returned_values = "\n".join(files_array)
        return "N0TSenDed " + returned_values