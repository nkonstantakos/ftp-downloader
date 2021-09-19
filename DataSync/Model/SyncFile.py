class SyncFile:

    def __init__(self, file_name: str, file_path: str, full_file_path: str, size: int):
        self.file_name = file_name
        self.file_path = file_path
        self.full_relative_path = "{0}/{1}".format(file_path[1:], file_name)
        self.full_file_path = "{0}/{1}".format(full_file_path, file_name)
        self.size = size
