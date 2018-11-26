import threading
import logging
import signal

from football import Football

logging.basicConfig(level=logging.INFO)
threads = []
e = threading.Event()

def quit(signo, _frame):
    print "Interrupted by %d, shutting down" % signo 
    e.set()

def main():
    plugins = [Football("steelers"), Football("seahawks")]
    while not e.isSet():
        for plugin in plugins:
            if plugin.check():
                plugin.trigger()
        e.wait(30)

for sig in ('TERM', 'HUP', 'INT'):
    signal.signal(getattr(signal, 'SIG'+sig), quit)

main()