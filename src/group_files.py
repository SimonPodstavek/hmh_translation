import os

import path
import shutil


paths = []

directory_path = r'C:\Users\Asus\Desktop\preklad\KL_preklady doc'




def iterate_files_in_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            new_path = filename.split()[0]
            # Do something with the file_path, for example:


            if not os.path.exists(os.path.join(r'C:\Users\Asus\Desktop\preklad\KL_preklady doc\documents_by_version',new_path)):
                os.mkdir(os.path.join(r'C:\Users\Asus\Desktop\preklad\KL_preklady doc\documents_by_version',new_path))

            destination_path = '\\'.join([r'C:\Users\Asus\Desktop\preklad\KL_preklady doc\documents_by_version',new_path,filename])
            shutil.move(file_path, destination_path)

    print(1)


iterate_files_in_directory(directory_path)
