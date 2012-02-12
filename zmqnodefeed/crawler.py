import difflib
import threading
import publisher
import time

class Crawler(threading.Thread):
    def __init__(self, watch='playbyplay.txt', interval=5, *args, **kwargs):
        super(Crawler, self).__init__(*args, **kwargs)
        self.watchfile = watch
        self.interval = interval
        self.last_snapshot = []
        self.publisher = publisher.Publisher()
       
    def run(self):
        self.publisher.publish('ready')
        time.sleep(1)

        while True:
            current_snapshot = open(self.watchfile).readlines()

            diff = difflib.ndiff(self.last_snapshot, current_snapshot)
            diff = [ x for x in diff if not x.startswith('?') ]

            # let's do some compression on diff
            num_diff = 0
            for i in range(len(diff)):
                num_diff += 1
                if diff[i].startswith(' '):
                    diff[i] = '=\n'
                    num_diff -= 1
                elif diff[i].startswith('-'):
                    diff[i] = '-\n'

            if num_diff:
                self.publisher.publish( ''.join(diff) )

            self.last_snapshot = current_snapshot
            time.sleep(self.interval)
    
if __name__ == "__main__":
    c = Crawler(watch='playbyplay.txt',interval=5)
    c.setDaemon(True)
    c.start()
    c.join()
