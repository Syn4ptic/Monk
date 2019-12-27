import os
import sys
import time
import logging
import errno
import shutil
from time import sleep
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

# Set below to true if you want to create extension folders eg. Documents/doc
extension_folders = False

# Formats and filder names can be set below 
docs_formats = ['doc', 'odt', 'pdf' , 'rtf', 'tex', 'txt', 'wks', 'wpd', 'docx', 'vsdx', 'vsd']
docs_name = 'Documents'
audio_formats = ['aif', 'cda', 'mid', 'midi', 'mp3', 'mpa', 'ogg', 'wav', 'wma', 'wpl']
audio_name = 'Audio'
compression_formats = ['7z', 'arj', 'deb', 'pkg', 'rar', 'rpm', 'tar', 'gz', 'tar.gz', 'z', 'zip']
archives_name = 'Archives'
discimage_formats = ['bin', 'dmg', 'iso', 'toast', 'vcd']
discimage_name = 'Images'
data_formats = ['csv', 'dat', 'db', 'dbf', 'log', 'mdb', 'sav', 'sql', 'tar', 'xml']
data_names = 'Data'
exec_formats = ['apk', 'bat', 'cgi', 'pl', 'com', 'exe', 'gadget', 'jar', 'py', 'wsf', 'msi']
exec_names = 'Applications'
font_formats = ['fnt', 'fon', 'otf', 'ttf']
font_names = 'Fonts'
image_formats = ['ai', 'bmp', 'gif', 'ico', 'jpeg', 'jpg', 'png', 'ps', 'psd', 'svg', 'tif', 'tiff', 'xcf']
image_names = 'Images'
internet_formats = ['ps1','har','asp', 'aspx', 'cer', 'cfm', 'cgi', 'css', 'htm', 'html', 'js', 'jsp', 'part', 'php', 'py', 'rss', 'xhtml', 'c', 'class', 'cpp', 'cs', 'h', 'java', 'sh', 'swift', 'vb' ]
internet_names = 'Programing'
presentation_formats = ['key', 'odp', 'pps', 'ppt', 'pptx']
presentation_names = 'Presentations'
spreadsheet_formats = ['ods', 'xlr', 'xls', 'xlsx', 'xlsm']
spreadsheet_names = 'Spreadsheets'
system_formats = ['bak', 'cab', 'cfg', 'cpl', 'cur', 'dll', 'dmp', 'drv', 'icns', 'ico', 'ini', 'ink', 'sys', 'tmp' ] 
system_names = 'System Files'
video_formats = ['3g2', '3gp', 'avi', 'flv', 'h264', 'm4v', 'mkv', 'mov', 'mp4', 'mpg', 'mpeg', 'rm', 'swf', 'vob', 'wmv']
video_names = 'Video'
message_formats = ['eml', 'msg']
message_names = 'Messages'


def check_filetype(ext):   #Checks for filetype and after that will return desire folder name 
    if ext[1:] in docs_formats:
        return(docs_name)
    elif ext[1:] in audio_formats:
        return(audio_name)
    elif ext[1:] in compression_formats:
        return(archives_name)
    elif ext[1:] in discimage_formats:
        return(discimage_name)
    elif ext[1:] in data_formats:
        return(data_names)
    elif ext[1:] in exec_formats:
        return(exec_names)
    elif ext[1:] in font_formats:
        return(font_names)
    elif ext[1:] in image_formats:
        return(image_names)
    elif ext[1:] in internet_formats:
        return(internet_names)
    elif ext[1:] in presentation_formats:
        return(presentation_names)
    elif ext[1:] in spreadsheet_formats:
        return(spreadsheet_names)
    elif ext[1:] in system_formats:
        return(system_names)
    elif ext[1:] in video_formats:
        return(video_names)
    elif ext[1:] in message_formats:
        return(message_names)
    else:
        return('None')



def gather_files():
    everything = os.listdir(path)
    all_files = [];
    for i in everything:
        if os.path.isfile(os.path.join(path, i)):
            all_files.append(str(os.path.join(path, i)))
    return all_files
    
def filecheck(f):
    try:
        with open(f) as file:
            pass
        return True
    except IOError as e:
        # print(e.errno)
        if e.errno == 2:
            return 'Missing'
        else:
            return False






class Event(LoggingEventHandler):
    def on_modified(self, event):
        files = gather_files()
        for f in files:
            file_path, ext = os.path.splitext(f)
            full_path = file_path+ext
            file_type = check_filetype(ext)
            filename = Path(full_path).stem
            if extension_folders == True:
                destination_path = str(os.path.join(path, file_type, ext[1:]))  
            else: 
                destination_path = str(os.path.join(path, file_type)) 
            move_files(file_type, ext, full_path, destination_path, filename)

    def on_created(self, event):
        file_path, ext = os.path.splitext(event.src_path)
        full_path = file_path+ext
        file_type = check_filetype(ext)
        filename = Path(full_path).stem
        if extension_folders == True:
            destination_path = str(os.path.join(path, file_type, ext[1:]))  
        else: 
            destination_path = str(os.path.join(path, file_type)) 
        move_files(file_type, ext, full_path, destination_path, filename)
        # print(gather_files())
    def on_moved(self, event):
        files = gather_files()
        for f in files:
            file_path, ext = os.path.splitext(f)
            full_path = file_path+ext
            file_type = check_filetype(ext)
            filename = Path(full_path).stem
            if extension_folders == True:
                destination_path = str(os.path.join(path, file_type, ext[1:]))  
            else: 
                destination_path = str(os.path.join(path, file_type))  
            move_files(file_type, ext, full_path, destination_path, filename)


            

def move_files(file_type, ext, full_path, destination_path, filename):
    print(file_type)
    if file_type == "None":
        pass
    else:    

        try:
            os.makedirs(os.path.join(path, str(file_type)))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        if extension_folders == True:                     
            try:
                os.makedirs(os.path.join(path, str(file_type), ext[1:]))

            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        try:
            print(full_path)
            while not filecheck(full_path):
                time.sleep(5)
                print(filecheck(full_path))
            if filecheck(full_path) == 'Missing':
                print('File is missing skipping...')
            else:
                shutil.move(full_path, destination_path)
        
        except OSError as e:
            if e.errno != errno.EEXIST:
                num = 1
                while True: 
                    if extension_folders == True:
                        new_name = os.path.join(path, str(file_type), ext[1:] ,filename + '(' + str(num) + ')'+ ext)
                    else:
                        new_name = os.path.join(path, str(file_type),  filename + '(' + str(num) + ')'+ ext)
                          
                    if not os.path.exists(new_name):
                        print(new_name)
                        while not filecheck(full_path):
                            time.sleep(5)
                            print(filecheck(full_path))
                        if filecheck(full_path) == 'Missing':
                            print('File is missing skipping...')
                            break
                        else:
                            shutil.move(full_path, new_name)
                            break 
                    num = num + 1
                


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # path = r"C:\Users\marcin.kawka\OneDrive - DSV\Desktop\DEVStuff\Monk\Testfolder"
    path = r"C:\Users\marcin.kawka\OneDrive - DSV\Desktop"
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
    