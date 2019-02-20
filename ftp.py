hostname = '****'
username = '****'
password = '***'
start_directory = '/'
backup_dir = 'C:\\backup'

import ftplib
import os
import datetime

def get_files_directories():

    dirlisting = []
    
    ftp_obj.retrlines('LIST',callback=dirlisting.append)
    
    files = []
    directories = []
    
    for l in dirlisting:
        lastspace = l.rindex(' ')
        file_name = l[lastspace+1:]
        if l[0] == 'd':
            directories.append(file_name)
        elif l[0] == '-':
            files.append(file_name)
            
    return files,directories
    
def backup_directory(local_dir,remote_dir):

    os.chdir(local_dir)
    ftp_obj.cwd(remote_dir)
    print('In directory '+remote_dir)

    files,directories = get_files_directories()

    for f in files:
        print('Backing up '+f)
        try:
            ftp_obj.retrbinary('RETR '+f, open(f, 'wb').write)
        except ftplib.error_perm:
            print('Skipping '+f+' due to permissions')
        
    for d in directories:
        newremote = remote_dir+d+'/'
        newlocal = local_dir+'\\'+d
        os.mkdir(newlocal)
        backup_directory(newlocal,newremote)
        


os.chdir(backup_dir)



datestring = str(datetime.date.today())

os.mkdir(datestring)
os.chdir(datestring)
local_dir = os.getcwd()



ftp_obj = ftplib.FTP(host=hostname, user=username, passwd=password)



remote_dir = start_directory

backup_directory(local_dir,remote_dir)



ftp_obj.quit()
