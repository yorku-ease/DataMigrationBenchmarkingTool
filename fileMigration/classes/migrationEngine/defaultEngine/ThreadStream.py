import threading


class ThreadStream(threading.Thread):
    def __init__(self, target,streamNumber,local_file_path,remote_file_path,compressionType,limit):
        self.streamNumber = streamNumber
        self.local_file_path = local_file_path
        self.remote_file_path = remote_file_path
        self.compressionType = compressionType
        self.limit = limit
        super().__init__(target=target,args=(local_file_path,remote_file_path,compressionType,limit,streamNumber),name = streamNumber)
        self._return_value = None

    def run(self):
        if self._target is not None:
            self._return_value = self._target(self.local_file_path,self.remote_file_path,self.compressionType,self.limit,self.streamNumber)

    def join(self):
        super().join()
        return self._return_value