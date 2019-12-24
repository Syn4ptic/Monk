import os
import sys
import time
import logging
import errno
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler



docs_formats = ['doc', 'odt', 'pdf' , 'rtf', 'tex', 'txt', 'wks', 'wpd', 'docx']

def gather_files():
    all_files = os.listdir()
    return all_files
    


def check_filetype(ext):   #Checks for filetype and after that will return desire folder name 
    if ext[1:] in docs_formats:
        return('Documents')
    else:
        return('None')



class Event(LoggingEventHandler):
    def on_modified(self, event):
        file_path, ext = os.path.splitext(event.src_path)
        full_path = file_path+ext
        file_type = check_filetype(ext)
        filename = Path(full_path).stem
        destination_path = str(os.path.join(os.getcwd(), file_type, ext[1:]))
        

    def on_created(self, event):
        file_path, ext = os.path.splitext(event.src_path)
        full_path = file_path+ext
        file_type = check_filetype(ext)
        filename = Path(full_path).stem
        destination_path = str(os.path.join(os.getcwd(), file_type, ext[1:]))
        move_files(file_type, ext, full_path, destination_path, filename)
        print(gather_files())
                

def move_files(file_type, ext, full_path, destination_path, filename):
    print(file_type)
    if file_type == "None":
        print('Ext not found')
    else:    

        try:
            os.makedirs(str(file_type))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        try:
            os.makedirs(os.path.join(str(file_type), ext[1:]))

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        try:
            shutil.move(full_path, destination_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                print('File_exist')
                num = 1
                # new_name = os.path.join(os.getcwd(), str(file_type), ext[1:], filename + '(' + str(num) + ')'+ ext)
                # new_name = os.path.join(os.getcwd(), str(file_type), ext[1:] , filename + '(' + str(num) + ')'+ ext)
                # print(new_name)
                while True:      
                    new_name = os.path.join(os.getcwd(), str(file_type), ext[1:] , filename + '(' + str(num) + ')'+ ext)      
                    if not os.path.exists(new_name):
                        shutil.move(full_path, new_name)
                        break 
                    num = num + 1
                


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = os.getcwd()
    print(path)
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    