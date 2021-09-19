import ftplib
import os

from DataSync.Model.SyncFile import SyncFile


class FileDownloader:

    def __init__(self, local_root: str, ftp: ftplib.FTP, file: SyncFile):

        self.local_root = local_root
        self.ftp = ftp
        self.file = file
        self.destination_path = "{0}/{1}".format(local_root, file.full_relative_path)

        self.ftp.sendcmd("TYPE i")
        self.size = self.ftp.size(self.file.full_file_path)

    def download(self, dry_run: bool):
        if not dry_run:
            self.ftp.retrbinary("RETR " + self.file.full_file_path, self.file_write)
        else:
            print("Write file {0} to {1}".format(self.file.full_file_path, self.destination_path))

    def file_write(self, data):
        os.makedirs(os.path.dirname(self.destination_path), exist_ok=True)
        new_file = open(self.destination_path, 'ab')
        new_file.write(data)
        new_file.close()

