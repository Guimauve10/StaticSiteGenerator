import os
import shutil

from constants import *
from textnode import TextNode, TextType
from gencontent import generate_page

def main():
    delete_public_files()
    copy_file_from_path(STATIC_LOCATION, PUBLIC_LOCATION)
    generate_page(os.path.join(CONTENT_LOCATION, "index.md"), TEMPLATE_LOCATION, os.path.join(PUBLIC_LOCATION, "index.html"))

def delete_public_files():
    print("Deleted public folder")
    if os.path.exists(PUBLIC_LOCATION):
        shutil.rmtree(PUBLIC_LOCATION)
    return

def copy_file_from_path(path, dest):
   if not os.path.exists(dest):
       os.mkdir(dest)
   path_dir = os.listdir(path)
   print(f"{path} contains: {path_dir}")
   for element in path_dir:
        new_path = os.path.join(path, element)
        new_dest = os.path.join(dest, element)
        print(f"Copying {new_path} to {new_dest}")
        if os.path.isfile(new_path):
           shutil.copy(new_path, new_dest)
        
        if os.path.isdir(new_path):
           copy_file_from_path(new_path,new_dest)
    
   return 

main()