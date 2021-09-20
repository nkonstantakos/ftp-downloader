import ftplib
import configparser

from DataSync.FTP.FileDownloader import FileDownloader
from DataSync.Model.SyncFile import SyncFile


class FTPHandler:

    def __init__(self, config: configparser.ConfigParser):
        self.config = config
        self.ftp = ftplib.FTP(self.config['FTP']['url'])
        self.remote_download_folder = config['FTP']['remoteRoot']

    def get_remote_files(self):
        try:
            self.ftp.cwd(self.remote_download_folder)
        except ftplib.error_perm as resp:
            if str(resp) == "550 No files found":
                print("No files in this directory")
            else:
                raise

        remote_files = []
        self.list_recursive(self.remote_download_folder, remote_files)
        return remote_files

    def list_recursive(self, remote_dir, files):
        try:
            self.ftp.cwd(remote_dir)
        except ftplib.error_perm as resp:
            if str(resp) == "550 No files found":
                print("No files in this directory")
            else:
                raise
        for entry in self.ftp.mlsd():
            if entry[1]['type'] == 'dir':
                remote_path = remote_dir + "/" + entry[0]
                self.list_recursive(remote_path, files)
            elif entry[1]['type'] == 'file':
                files.append(SyncFile(entry[0], remote_dir.replace(self.remote_download_folder, ''), remote_dir,
                                      int(entry[1]['size'])))

    def download_file(self, file: SyncFile, dry_run: bool = False):
        downloader = FileDownloader(self.config['FTP']['localRoot'], self.ftp, file)
        downloader.download(dry_run)

    def login(self):
        self.ftp.login(self.config['FTP']['username'], self.config['FTP']['password'])

    def close(self):
        self.ftp.close()
