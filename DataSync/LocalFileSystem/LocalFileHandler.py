import configparser
import os

from DataSync.Model.SyncFile import SyncFile


class LocalFileHandler:

    def __init__(self, config: configparser.ConfigParser):
        self.config = config
        self.local_root = config['FTP']['localRoot']

    def get_local_files(self):
        local_files: list[SyncFile] = []
        for path, sub_dirs, files in os.walk(self.local_root):
            for name in files:
                local_files.append(SyncFile(name, path.replace(self.local_root, ''), path, 0))
        return local_files
