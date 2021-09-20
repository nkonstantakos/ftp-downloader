import configparser
import os

from pathlib import Path, PureWindowsPath, PurePosixPath, PurePath
from DataSync.FTP.FTPHandler import FTPHandler
from DataSync.Model.SyncFile import SyncFile
from DataSync.LocalFileSystem.LocalFileHandler import LocalFileHandler


class DataSyncHandler:

    def __init__(self, config: configparser.ConfigParser, dry_run: bool):
        self.config = config
        self.dry_run = dry_run
        self.ftp_handler = FTPHandler(config)
        self.local_handler = LocalFileHandler(config)

    def sync_data(self):
        self.ftp_handler.login()
        remote_files: list[SyncFile] = self.ftp_handler.get_remote_files()
        local_files: list[SyncFile] = self.local_handler.get_local_files()
        new_files: list[SyncFile] = self.discover_new_files(local_files, remote_files)
        self.download_new_files(new_files)
        self.ftp_handler.close()

    def discover_new_files(self, local_files: list[SyncFile], remote_files: list[SyncFile]):
        new_files: list[SyncFile] = []
        for remote_file in remote_files:
            existing = False
            for local_file in local_files:
                if self.files_match(local_file, remote_file):
                    existing = True
                    break
            if not existing:
                new_files.append(remote_file)
        return new_files

    def files_match(self, local: SyncFile, remote: SyncFile):
        return local.file_name == remote.file_name and PurePath(local.file_path) == PurePath(remote.file_path)

    def print_all(self, header: str, all_items: list[SyncFile]):
        print(header)
        for item in all_items:
            print('Path: {0} FileName: {1} FullPath: {2}'.format(item.file_path, item.file_name, item.full_file_path))

    def download_new_files(self, new_files: list[SyncFile]):
        for file in new_files:
            self.ftp_handler.download_file(file, dry_run=self.dry_run)
