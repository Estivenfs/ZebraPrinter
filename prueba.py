from zebra import Zebra
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
import sys
import configparser
import subprocess
#https://www.youtube.com/watch?v=ojMTl_1MHYs
app_path = os.path.dirname(sys.executable)
def print_zpl(zpl):
    z = Zebra( )
    impresoras = z.getqueues()
    #Para prueba en casa comentar en produccion
    #impresoras.append('ZDesigner Hola')
    print_exist=False
    for printer in impresoras:
        if('ZDESIGNER' in printer.upper()):
            print_exist=True
            z.setqueue( printer )
            break
    if(not print_exist):
        print('No existe impresora que contenga ZDesigner en el nombre...')
    
    if(print_exist and zpl!=''):
        #Descomentar para produccion
        print(zpl)
        z.output( zpl )
        

    if(zpl==''):
        print('No hay contenido para imprimir...')
#Abre el archivo ejecutable para generar los archivos    
def openExe():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    fileName = config['DEFAULT']['FILE_NAME']
    exe = subprocess.Popen(fileName)

def obtain_folder():
    return os.listdir()

def create_folder(dir):
    if 'toPrint' not in dir:
        os.mkdir('toPrint')
        print('Carpeta creada...')

def print_all_files(dir):
    files=os.listdir(dir)
    some_file=False
    for file in files:
        name , exten = os.path.splitext(file)
        if(exten=='.txt'):
            some_file=True
            my_path=dir + '/' + file
            with open(my_path,"r",encoding="utf-8") as zpl_text:
                if not zpl_text.closed:
                    print_zpl(zpl_text.read())
                

            os.remove(my_path)
    if(not some_file):
        print('No habia archivo para imprimir en: '+dir)



dir=obtain_folder()
create_folder(dir)
print(app_path)
print_all_files('./toPrint')
openExe()







class MyEventHandler(FileSystemEventHandler):

    def on_modified(self, event):
        print(event.src_path, "modificado.")
    
    def on_created(self, event):
        time.sleep(2)
        print(event.src_path, "creado.")
        print_all_files('./toPrint')
        
    
    def on_moved(self, event):
        print(event.src_path, "movido a", event.dest_path)
    
    def on_deleted(self, event):
        print(event.src_path, "eliminado.")

observer = Observer()
observer.schedule(MyEventHandler(), "./toPrint", recursive=False)
observer.start()
try:
    while observer.is_alive():
        observer.join(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()