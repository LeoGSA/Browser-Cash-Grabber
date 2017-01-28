# -*- coding: <utf-8> -*-

## Mozilla (or any other browser) cache grabber by LeoGSA (leogsa@gmail.com)
##
## A tiny, but very usefull programm for grabbing cache folders of different browsers.
## It also can be used for file recovery processes, when you need to sort files with lost extentions.
##
## There are a few configuration parameters.

# EXPLANATIONS:

# from_folder:
# in from_folder specify the cache folder of your browser OR folder, containing files without extentions - do not put '/' at the end
# RUSSIAN: указывать без слеша в конце Ваня комп

# to_folder:
# to_folder - is the destination folder - the place where you want your recognized files - do not put '/' at the end
# RUSSIAN: указывать без слеша в конце  'I:/30'

# min_size:
# min_size - minimal file-size (in bits) in cache which you are interested in (files of smaller size than this will be deleted without analysis)
# RUSSIAN:минимальный размер файла в кэше (которые нас интересуют) 26000

# folder_list:
# in folder_list leave only those elements which you are interested in, always leave the fist blank element
# (file types which are not in this list will not be recognized)
# This is the example of maximum availiable list for the moment:
# folder_list = ['','/jpg',"/png","/gif_87","/gif_89","/video","/music",'/html','/moof',"/doc","/pdf","/zip"]
# At the monent:
# "/music" means .mp3 files
# "/video" means .mp4 .avi and .flv files
# e.g. if you want .mp3 and .jpg to be grabbed, your folder_list should be: folder_list = ['','/jpg',"/music"]

# save_unknown
# if this option is set to True, unknown (unrecognized) files with size
# bigger than min_size will be put to folder 'unknown' inside of to_folder

# print_unknown_header:
# if this option is set to True, unknown file headers will be printed during execution

# clear_from_folder_afterall:
# deletes and re-creates (clesrs) from_folder after all work is done

# from_folder='c:/Users/Ivan/AppData/Local/Mozilla/Firefox/Profiles/kp10flzc.default-1466620470116/cache2/entries'
from_folder='i:/66'
to_folder='i:/32-new'
min_size=26000
folder_list = ['','/jpg',"/png","/gif_87","/gif_89","/video"]
save_unknown = False
print_unknown_header = False
clear_from_folder_afterall = False

#
# NO USER SERVICEABLE PARTS BELOW HERE...
#


import os
import shutil
import sys


def make_folders(folder_list, to_folder):

    for i in folder_list:
        if os.path.isdir (to_folder+i)==False:
            os.mkdir (to_folder+i)

def analize_files(from_folder, folder_list):

    # matrix legend: [element in folder_list, header marker, subfolder for to_folder, extention]
    full_matrix = [

        ['/jpg', r'\xff\xd8\xff', '/jpg/', '.jpg'],
        ['/jpg', 'Exif', '/jpg/', '.Jpeg'],
        ['/jpg', 'JFIF', '/jpg/', '.Jpeg'],
        ['/gif_87', 'GIF87', '/gif_87/', '.gif'],
        ['/gif_89', 'GIF89', '/gif_89/', '.gif'],
        ['/png', 'PNG', '/png/', '.png'],
        ['/video', 'ftyp', '/video/', '.mp4'],
        ['/video', 'FLV', '/video/', '.flv'],
        ['/video', 'AVI LIST', '/video/', '.avi'],
        ['/music', 'ID3', '/music/', '.mp3'],
        ['/html', '!DOCTYPE html', '/html/', '.html'],
        ['/moof', 'moof', '/moof/', '.moof'],
        ['/doc', r'\xd0\xcf\x11\xe0\xa1', '/doc/', '.doc'],
        ['/pdf', 'PDF', '/pdf/', '.pdf'],
        ['/zip', 'PK'+r'\x03\x04', '/zip/', '.zip']
    ]

    temp_matrix=[]
    for i in full_matrix:
        if i[0] in folder_list:
            temp_matrix.append(i)

    file_list=(d for d in os.listdir(from_folder))

    for i in file_list:
        if (os.path.getsize(from_folder+"/"+i))>min_size:
            with open (from_folder+"/"+i, "rb") as myfile:
                header=str(myfile.read(24))
            for y in temp_matrix:
                if y[0] in folder_list and y[1] in header:
                    shutil.move (from_folder+"/"+i,to_folder+y[2]+i+y[3])
                    not_recognized = False
                    break
                not_recognized = True
            if not_recognized and print_unknown_header:
                print (header)
            if not_recognized and save_unknown:
                shutil.move (from_folder+"/"+i,to_folder+"/"+i)

def del_and_create_from_folder(from_folder):
    shutil.rmtree(from_folder)
    assert(os.path.isdir(from_folder) == False)
    os.mkdir (from_folder)

if __name__ == '__main__':
    print ("Started")
    make_folders(folder_list=folder_list, to_folder=to_folder)
    analize_files(from_folder=from_folder, folder_list=folder_list)
    if clear_from_folder_afterall:
        del_and_create_from_folder(from_folder=from_folder)
    print ("Done!")
