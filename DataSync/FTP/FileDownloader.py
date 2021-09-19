import ftplib
import configparser


class FileDownloader:

    def __init__(self, config: configparser.ConfigParser, ftp: ftplib.FTP, remote_file_path: str, local_file_path: str,
                 dry_run: bool):

        self.config = config
        self.ftp = ftp
        self.remote_file_path = remote_file_path
        self.local_file_path = local_file_path
        self.dry_run = dry_run

        self.ftp.sendcmd("TYPE i")
        self.size = self.ftp.size(remote_file_path)

    def download(self):
        if not self.dry_run:
            self.ftp.retrbinary("RETR " + self.remote_file_path, self.file_write)
        else:
            print("Write file {0} to {1}".format(self.remote_file_path, self.local_file_path))

    def file_write(self, data):
        file = open(self.local_file_path, 'ab')
        file.write(data)
        file.close()

