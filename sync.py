import os
import hashlib
from os import listdir
from os.path import isfile, join
from shutil import copyfile

path1 = input('insert first folder (abs walk): ')
path2 = input('insert second folder (abs walk): ')

#checks if directiories are valid
path1 = path1.replace('\"', '')
path1 = os.path.join(path1, '')
path2 = path2.replace('\"', '')
path2 = os.path.join(path2, '')

if(not os.path.isdir(path1) or not os.path.isdir(path2)):
    print('\033[91myou have to insert valid directiories!\033[0m')
    exit()

files1 = []
files2 = []
error_count = 0
print('\33[7mLOADING...\033[0m')
#calculates MD5 digest
def getDigest(file_location):
    try:
        md5_hash = hashlib.md5()
        a_file = open(file_location, "rb")
        content = a_file.read()
        md5_hash.update(content)
        digest = md5_hash.hexdigest()
        return digest
    except Exception:
        error_count += 1
        print('failed calculating MD5 digest of \33[101m' + file_location + '\033[0m')

class OnlyFile:
    def __init__(self, name, file_location, cut_path, creation, last_mod):
        """ constructor
        Args:
            name (str): only the name of the file (example.exe)
            file_location (str): absolute walk of file
            cut_path (str): absolute walk from the path inserted, for example /folder_inside/photos from D:Desktop/folder_inside/photos
            creation ([float]): file's creation date (in this version is not used but it's kept for future purposes)
            last_mod ([float]): file's last modification date
        """
        self.name = name
        self.file_location = file_location
        self.cut_path = cut_path
        self.creation = creation
        self.last_mod = last_mod
        self.new = True
        if(self.cut_path != ''):
            self.cut_path_name = os.path.join(self.cut_path, self.name)
        else:
            self.cut_path_name = self.name
            
    def is_new(self):
        return self.new
    
    def __repr__(self):
        return 'name:%s file_location:%s cut_path:%s cut_path_name:%s creation:%s last_mod:%s' % (self.name, self.file_location, self.cut_path, self.cut_path_name, self.creation, self.last_mod)

# populate the 2 arrays with OnlyFiles objects
for path, dirs, files in os.walk(path1):
    for name in files:
        #entire file location (absolute)
        file_location = os.path.join(path, name)
        try:
            #inserts the file in the array
            cut_path = path.replace(path1, '')
            temp_file = OnlyFile(name, file_location, cut_path, os.path.getctime(file_location), os.path.getmtime(file_location))
            files1.append(temp_file)
        except Exception:
            error_count += 1
            print('failed to open \33[101m' + file_location + '\033[0m')
 
for path, dirs, files in os.walk(path2):
    for name in files:
        file_location = os.path.join(path, name)
        try:
            cut_path = path.replace(path2, '')
            temp_file = OnlyFile(name, file_location, cut_path, os.path.getctime(file_location), os.path.getmtime(file_location))
            files2.append(temp_file)
        except Exception:
            error_count += 1
            print('failed to open \33[101m' + file_location + '\033[0m')

# check if 2 files are present in the same locations in the 2 folders and copies the newer one only if MD5 digest is not the same
print('\033[95mlog:\033[0m')
print('\33[7mchecking md5 of same files, don\'t close\033[0m')
same_digest_count = 0
different_digest_count = 0
for file1 in files1:
    for file2 in files2:
        if(file1.name == file2.name and file1.cut_path == file2.cut_path):
            digest1 = getDigest(file1.file_location)
            digest2 = getDigest(file2.file_location)
            file1.new = False
            file2.new = False
            if(digest1 != digest2):
                if(file1.last_mod > file2.last_mod):
                    try:
                        os.remove(file2.file_location)
                        copyfile(file1.file_location, file2.file_location)
                        different_digest_count += 1
                        print('updated \033[1m\033[92m' + file2.name + '\033[0m inside of \033[4m' + path2 + file2.cut_path + '\033[0m (digest was different)')
                    except Exception:
                        error_count += 1
                        print('!!! NOT COPIED \33[101m' + file1.name + '\33[0m to ' + path2 + file2.cut_path + ' !!!')
                else: #file1.last_mod < file2.last_mod
                    try:
                        os.remove(file1.file_location)
                        copyfile(file2.file_location, file1.file_location)
                        different_digest_count += 1
                        print('updated \033[1m\033[92m' + file1.name + '\033[0m inside of \033[4m' + path1 + file1.cut_path + '\033[0m (digest was different)')
                    except Exception:
                        error_count += 1
                        print('!!! NOT COPIED \33[101m' + file2.name + '\33[0m to ' + path1 + file1.cut_path + ' !!!')
            else:
                same_digest_count += 1
                #print('same MD5 digest for file \033[1m\033[92m' + file1.name + '\033[0m')
print('\33[7mfinished checking equal files, \033[95m' + str(same_digest_count) + '\033[0m\33[7m with the same digest and \033[95m' + str(different_digest_count) + '\033[0m\33[7m with different digest, now creating non-existing ones\033[0m')

#copies the files not present in both folders in the one where are missing
created_count = 0
for file in files1:
    if(file.is_new()):
        new_location = path2 + file.cut_path
        created_count += 1
        if(os.path.isdir(new_location)):
            try:
                copyfile(file.file_location,  os.path.join(new_location, file.name))
                print('created new file \033[1m\033[92m' + file.name + '\033[0m inside of \033[4m' + new_location + '\033[0m')
            except Exception:
                error_count += 1
                print('!!! NOT COPIED \33[101m' + file1.name + '\33[0m!!! (new file)')
        else:
            try:
                os.makedirs(path2 + file.cut_path, exist_ok=True)
                copyfile(file.file_location,  os.path.join(new_location, file.name))
                print('created new directory \033[4m' + new_location + '\033[0m and copied file \033[1m\033[92m' + file.name + '\033[0m')
            except Exception:
                error_count += 1
                print('!!! NOT COPIED \33[101m' + file1.name + '\33[0m!!! (new file)')

for file in files2:
    if(file.is_new()):
        new_location = path1 + file.cut_path
        created_count += 1
        if(os.path.isdir(new_location)):
            try:
                copyfile(file.file_location,  os.path.join(new_location, file.name))
                print('created new file \033[1m\033[92m' + file.name + '\033[0m inside of \033[4m' + new_location+ '\033[0m')
            except Exception:
                error_count += 1
                print('!!! NOT COPIED \33[101m' + file2.name + '\33[0m!!! (new file)')
        else:
            try:
                os.makedirs(path1 + file.cut_path, exist_ok=True)
                copyfile(file.file_location,  os.path.join(new_location, file.name))
                print('created new directory \033[4m' + new_location + '\033[0m and copied file \033[1m\033[92m' + file.name + '\033[0m')
            except Exception:
                error_count += 1
                print('!!! NOT COPIED \33[101m' + file2.name + '\33[0m!!! (new file)')

print('\33[7m\033[95m' + str(different_digest_count + same_digest_count + created_count) + '\033[0m\33[7m total files, \033[95m' + str(different_digest_count) + '\033[0m\33[7m updated and \033[95m' + str(created_count) + '\033[0m\33[7m created\033[0m')
print('\33[7mfinished with \033[95m' + str(error_count) + '\33[0m\33[7m errors :)\33[0m')

'''
 $$$$$$\ $$$$$$$\ $$$$$$$$\ 
$$  __$$\$$  __$$\$$  _____|
$$ /  \__$$ |  $$ $$ |      
$$ |$$$$\$$ |  $$ $$$$$\    
$$ |\_$$ $$ |  $$ $$  __|   
$$ |  $$ $$ |  $$ $$ |      
\$$$$$$  $$$$$$$  $$ |      
 \______/\_______/\__|      
version 1.2
'''
