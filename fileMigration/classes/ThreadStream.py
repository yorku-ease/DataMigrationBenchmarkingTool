import threading


class ThreadStream(threading.Thread):
    def __init__(self, target, stream):
        self.stream = stream
        super().__init__(target=target,args=(stream),name = stream)
        self._return_value = None

    def run(self):
        #current_thread = threading.current_thread()
        #for i in range(1000):
        #    print("Thread", current_thread.name, "iteration", i)
        if self._target is not None:
            self._return_value = self._target(self.stream)

    def join(self):
        super().join()
        return self._return_value