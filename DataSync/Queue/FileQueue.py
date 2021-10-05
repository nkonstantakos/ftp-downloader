from DataSync.Model.Priority import Priority
from DataSync.Model.QueueItem import QueueItem
from DataSync.Model.SyncFile import SyncFile


class FileQueue:

    def __init__(self):
        self.queue: list[QueueItem] = list()

    def in_progress(self):
        return len(self.queue) > 0

    def add_item_to_queue(self, file: SyncFile):
        self.queue.append(QueueItem(file, Priority.NORMAL))

    def add_items_to_queue(self, files: list[SyncFile]):
        for file in files:
            self.queue.append(QueueItem(file, Priority.NORMAL))

    def remove_from_queue(self, file: SyncFile):
        removed_item: QueueItem = None
        for item in self.queue:
            if item.file == file:
                removed_item = item
        if removed_item is not None:
            self.queue.remove(removed_item)

    async def print_queue(self):
        if len(self.queue) > 0:
            message = "Files in Queue:\n"
            for i in range(len(self.queue)):
                current_file = self.queue[i].file
                message = message + "{0}. {1}/{2}\n".format(i + 1, current_file.file_path, current_file.file_name)
                if current_file.progress > 0:
                    pct = (current_file.progress / current_file.size) * 100
                    message = message + "Progress: {0}/{1} ({2}%)\n".format(current_file.progress, current_file.size, pct)
            return message
        return None
