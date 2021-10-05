from DataSync.Model.Priority import Priority
from DataSync.Model.SyncFile import SyncFile


class QueueItem:

    def __init__(self, file: SyncFile, priority: Priority):
        self.file = file
        self.priority = priority
