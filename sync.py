import os
from os import listdir
from os.path import isfile, join
from shutil import copyfile

path1 = input('insert first folder (abs walk): ')
path2 = input('insert second folder (abs walk): ')

# checks if directiories are valid
path1 = path1.replace('\"', '')
path2 = path2.replace('\"', '')
if(not os.path.isdir(path1) or not os.path.isdir(path2)):
    print('\033[91myou have to insert valid directiories!\033[0m')
    exit()

files1 = []
files2 = []

class OnlyFile:
    def __init__(self, name, file_location, cut_path, creation, last_mod):
        """ constructor
        Args:
            name (string): only the name of the file (example.exe)
            file_location (str): absolute walk of file
            cut_path (str): absolute walk from the path inserted, for example /folder_inside/photos from D:Desktop/folder_inside/photos
            creation ([float]): file's creation date
            last_mod ([float]): file's last modification date
        """
        self.name = name
        self.file_location = file_location
        self.cut_path = cut_path
        self.creation = creation
        self.last_mod = last_mod
        self.new = True
        if(self.cut_path != ''):
            self.cut_path_name = (self.cut_path + '\\' + self.name)
        else:
            self.cut_path_name = self.name
            
    def is_new(self):
        return self.new
    
    def __repr__(self):
        return 'name:%s file_location:%s cut_path:%s cut_path_name:%s creation:%s last_mod:%s' % (self.name, self.file_location, self.cut_path, self.cut_path_name, self.creation, self.last_mod)

# populate the 2 arrays with OnlyFiles objects
for path, dirs, files in os.walk(path1):
    for name in files:
        file_location = os.path.join(path, name)
        cut_path = path.replace(path1, '')
        temp_file = OnlyFile(name, file_location, cut_path, os.path.getctime(file_location), os.path.getmtime(file_location))
        files1.append(temp_file)
 
for path, dirs, files in os.walk(path2):
    for name in files:
        file_location = os.path.join(path, name)
        cut_path = path.replace(path2, '')
        temp_file = OnlyFile(name, file_location, cut_path, os.path.getctime(file_location), os.path.getmtime(file_location))
        files2.append(temp_file)

# check if 2 files are present in the same locations in the 2 folders and copies the newer one
print('\033[95mlog:\033[0m')
for file1 in files1:
    for file2 in files2:
        if(file1.name == file2.name and file1.cut_path == file2.cut_path):
            if(file1.last_mod > file2.last_mod):
                file1.new = False
                file2.new = False
                os.remove(file2.file_location)
                copyfile(file1.file_location, file2.file_location)
                print('updated \033[1m\033[92m' + file2.name + '\033[0m inside of \033[4m' + path2 + file2.cut_path + '\033[0m')
            else:
                if(file1.last_mod < file2.last_mod):
                    file1.new = False
                    file2.new = False
                    os.remove(file1.file_location)
                    copyfile(file2.file_location, file1.file_location)
                    print('updated \033[1m\033[92m' + file1.name + '\033[0m inside of \033[4m' + path1 + file2.cut_path + '\033[0m')

#copies the files not present in both folders in the one where are missing
for file in files1:
    if(file.is_new()):
        new_location = path2 + file.cut_path
        if(os.path.isdir(new_location)):
            copyfile(file.file_location, (new_location + '\\' + file.name))
            print('created new file \033[1m\033[92m' + file.name + '\033[0m inside of \033[4m' + new_location + '\033[0m')
        else:
            os.makedirs(path2 + file.cut_path, exist_ok=True)
            copyfile(file.file_location, (new_location + '\\' + file.name))
            print('created new directory \033[4m' + new_location + '\033[0m and copied file \033[1m\033[92m' + file.name + '\033[0m')

for file in files2:
    if(file.is_new()):
        new_location = path1 + file.cut_path
        if(os.path.isdir(new_location)):
            copyfile(file.file_location, (new_location + '\\' + file.name))
            print('created new file \033[1m\033[92m' + file.name + '\033[0m inside of \033[4m' + new_location+ '\033[0m')
        else:
            os.makedirs(path1 + file.cut_path, exist_ok=True)
            copyfile(file.file_location, (new_location + '\\' + file.name))
            print('created new directory \033[4m' + new_location + '\033[0m and copied file \033[1m\033[92m' + file.name + '\033[0m')

print('finished :)')

'''
 $$$$$$\ $$$$$$$\ $$$$$$$$\ 
$$  __$$\$$  __$$\$$  _____|
$$ /  \__$$ |  $$ $$ |      
$$ |$$$$\$$ |  $$ $$$$$\    
$$ |\_$$ $$ |  $$ $$  __|   
$$ |  $$ $$ |  $$ $$ |      
\$$$$$$  $$$$$$$  $$ |      
 \______/\_______/\__|      
version 1.0
'''
