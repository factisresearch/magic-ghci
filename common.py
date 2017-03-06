TRACE = False

import sys
import threading
import traceback
import time
import os

log_file = None

def init_logging(name):
    global log_file
    pid = os.getpid()
    path = '/tmp/%s_%d.log' % (name, pid)
    log_file = open(path, 'a')

def debug(str, level='DEBUG', to_stderr=False):
    now = time.time()
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
    full_str = '[%s %s] %s\n' % (time_str, level, str)
    if to_stderr:
        sys.stderr.write(full_str)
    log_file.write(full_str)
    log_file.flush()

def warn(str):
    debug(str, 'WARN', to_stderr=True)

def trace(str):
    if TRACE:
        debug(str, 'TRACE')

class ThreadResult:
    def __init__(self, thread_name):
        self.thread_name = thread_name
        self.result = None
        self.is_exception = False
        self.event = threading.Event()

    def __str__(self):
        return 'ThreadResult(thread_name=%s, result=%s, is_exception=%d)' % \
            (self.thread_name, self.result, self.is_exception)

    def signal(self, result, is_exception):
        self.result = result
        self.is_exception = is_exception
        self.event.set()

    def wait(self, timeout_seconds):
        self.event.wait(timeout_seconds)

    def is_finished(self):
        return self.event.is_set()

def wait_for_thread_results(results, timeout_seconds):
    for r in results:
        trace('waiting for %s' % r)
        r.wait(timeout_seconds)
        if r.is_finished():
            return (True, r)
    return (False, None)

def fork_thread(name, fun, daemon=True):
    result = ThreadResult(name)
    def wrapped_fun():
        thread_name = threading.current_thread().name
        try:
            res = fun()
            debug('Thread %s terminated without exception' % thread_name)
            result.signal(res, False)
        except Exception, e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            exc = traceback.format_exception(exc_type, exc_value, exc_traceback)
            warn('Thread %s terminated with exception: %s' % (thread_name, ''.join(exc)))
            result.signal(e, True)
    t = threading.Thread(target=wrapped_fun, name=name)
    t.setDaemon(daemon)
    t.start()
    return result
