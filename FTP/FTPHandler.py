import ftplib
import configparser

from FTP.FileDownloader import FileDownloader


class FTPHandler:

    def __init__(self, config: configparser.ConfigParser, dry_run: bool):
        self.config = config
        self.dry_run = dry_run
        self.ftp = ftplib.FTP(self.config['FTP']['url'])
        self.ftp.login(config['FTP']['username'], config['FTP']['password'])
        self.remote_download_folder = config['FTP']['remoteRoot']

    def scan_for_updates(self):
        try:
            self.ftp.cwd(self.remote_download_folder)
            files = self.ftp.nlst()
        except ftplib.error_perm as resp:
            if str(resp) == "550 No files found":
                print("No files in this directory")
            else:
                raise

        remote_files = self.get_all_dirs(self.remote_download_folder)
        self.print_all(remote_files)

    def download_file(self, file_path: str):
        downloader = FileDownloader(self.config, self.ftp, file_path, file_path, self.dry_run)
        downloader.download()

    def close(self):
        self.ftp.close()

    def get_dirs(self, folder=""):
        contents = self.ftp.nlst(folder)
        folders = []
        for item in contents:
            if "." not in item:
                folders.append(item)
        return folders

    def get_all_dirs(self, folder=""):
        dirs = []
        new_dirs = []

        new_dirs = self.get_dirs(folder)

        while len(new_dirs) > 0:
            for dir in new_dirs:
                dirs.append(dir.replace(self.remote_download_folder, ''))

            old_dirs = new_dirs[:]
            new_dirs = []
            for dir in old_dirs:
                for new_dir in self.get_dirs(dir):
                    new_dirs.append(new_dir)

        dirs.sort()
        return dirs

    def print_all(self, all_items):
        print("***PRINTING ALL ITEMS***")
        for dir in all_items:
            print(dir)
