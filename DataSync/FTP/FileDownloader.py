import ftplib
import configparser

from DataSync.Model.SyncFile import SyncFile


class FileDownloader:

    def __init__(self, config: configparser.ConfigParser, ftp: ftplib.FTP, file: SyncFile):

        self.config = config
        self.ftp = ftp
        self.file = file

        self.ftp.sendcmd("TYPE i")
        self.size = self.ftp.size(self.file.full_file_path)

    def download(self, dry_run: bool):
        if not dry_run:
            self.ftp.retrbinary("RETR " + self.file.file_path, self.file_write)
        else:
            print("Write file {0} to {1}".format(self.file.file_path, self.file.file_path))

    def file_write(self, data):
        new_file = open(self.file.file_path, 'ab')
        new_file.write(data)
        new_file.close()

