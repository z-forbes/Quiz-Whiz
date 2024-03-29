import threading
from time import sleep
import pypandoc
import os
from tqdm import tqdm
import re

def download():
    pypandoc.download_pandoc(targetfolder=os.path.join(os.getcwd(), "program/pandoc"), delete_installer=True) # abs path required on linux


def track():
    fsize = 31.2 # mb, random value around 30 to seem legit lol
    while True:
        path = [f for f in os.listdir(".") if re.fullmatch("pandoc-[0-9.]+-(?:linux|windows)-[0-9a-zA-Z_]+(?:\.tar\.gz|\.msi)", os.path.basename(f))]
        if len(path)>1:
            return
        if len(path)==1:
            path = path[0]
            break
    
    pbar = tqdm(total=fsize, unit="mb", ncols=100)
    while not os.path.exists("program/pandoc/COPYRIGHT.txt"):
        size = os.path.getsize(path)/1000000
        if size>fsize:
            size=fsize-1
        pbar.update(size-pbar.n)
        sleep(0.5)
    pbar.update(fsize-pbar.n)
    pbar.close()

 
if __name__ =="__main__":
    t1 = threading.Thread(target=download, )
    t2 = threading.Thread(target=track)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
 
    print("Installed!")