import os
import shutil
import tempfile
from urllib.request import urlopen
import gzip
import subprocess
import datetime
import time

def zip_results(path_to_folder, archive_name="archive"):
    if os.path.exists(path_to_folder + '/{}.zip'.format(archive_name)):
        os.remove(path_to_folder + '/{}.zip'.format(archive_name))

    with tempfile.TemporaryDirectory() as dirpath:
        archive_temp_path = shutil.make_archive(dirpath + '/' + archive_name, 'zip', path_to_folder)
        archive_path = shutil.move(archive_temp_path, path_to_folder)

    return archive_path