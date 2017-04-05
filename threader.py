import threading
import time
import sys


class worker_status:
    OK = 0
    ERROR = -1
    WAITING = 1
    PAUSED = 2
    FINISHED = 3
    DEAD = 4
    RUNNING = 5
    INIT = 999

workers = dict()

class worker_thread:

    def __init__(self, name, function, parameters, autostart=False, callback=None):
        assert name not in workers

        self.worker_status = worker_status.INIT
        self.name = str(name)
        self.status = {}
        self.function = function
        self.result = None
        self.callback = callback
        self.parameters = parameters
        workers[self.name] = {'worker': self, 'status': self.status, 'result': None}
        self.set_status(worker_status.INIT)
        if autostart:
            self.start()

    def start(self):
        threading.Thread(target=self.run_worker).start()

    def set_status(self, status):
        self.status = status
        workers[self.name]['status'] = status

    def set_result(self, result):
        self.result = result
        workers[self.name]['result'] = result

    def run_worker(self):

        self.set_status(worker_status.RUNNING)
        result = self.function(**self.parameters)

        self.set_result(result)
        self.set_status(worker_status.FINISHED)

        if self.callback is not None:
            self.callback(result)


def wait_for_results(worker_threads=None, worker_names=None):
    target_threads = []
    if worker_threads is not None:
        target_threads += [{'key': workers[worker]['worker'], 'worker': workers[worker]['worker']} for worker in workers if workers[worker]['worker'] in worker_threads]
    if worker_names is not None:
        target_threads += [{'key': worker, 'worker': workers[worker]['worker']} for worker in workers if worker in worker_names]

    ready = False
    while not ready:
        time.sleep(0.1)
        ready = True
        for thread in target_threads:
            if thread['worker'].status != worker_status.FINISHED:
                ready = False
                continue

    return {thread['key']: thread['worker'].result for thread in target_threads}
