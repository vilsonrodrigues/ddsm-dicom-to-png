import sys
import shutil

if __name__ == "__main__":
    """python zip_directory Dataset-DDSM-One-View DDSM-one-view"""
    path_directory = sys.argv[1]
    path_zip       = sys.argv[2]
    print('Start Ziping')
    shutil.make_archive(path_zip, format='zip', root_dir=path_directory)
    print('Finish')
  
