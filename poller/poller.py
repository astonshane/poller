import threading
import logging
import signal
import ConfigParser

from football import Football

logging.basicConfig(level=logging.INFO)
threads = []
e = threading.Event()

def quit(signo, _frame):
    print "Interrupted by %d, shutting down" % signo 
    e.set()

def main():
    config = ConfigParser.ConfigParser()
    config.readfp(open('poller.cfg'))

    plugins = []
    for team in config.get("football", "teams").split(','):
        plugins.append(Football(team, config))
    
    while not e.isSet():
        for plugin in plugins:
            if plugin.check():
                plugin.trigger()
        e.wait(30)

for sig in ('TERM', 'HUP', 'INT'):
    signal.signal(getattr(signal, 'SIG'+sig), quit)

main()