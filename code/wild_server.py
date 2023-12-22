#!/usr/bin/env python

# A simple threaded SocketServer exposing a WildDictionary to the network.

__author__ = 'Cian Synnott'
__copyright__ = 'Copyright 2011, Cian Synnott'
__license__ = 'MIT'

import SocketServer
import logging
import re
import sys
import threading
import time

from wild_dictionary import WildDictionary

# Global dictionary. I ain't proud, and making a SocketServer class that
# takes this as an argument is more pain than I feel like taking right now.
dictionary = None

# Ditto the log.
log = None

class WildHandler(SocketServer.BaseRequestHandler):
  def handle(self):
    """Handle a single wildcarded request.

    This is a very simple request handler following the SocketServer docs.
    We just take a string, do a tiny bit of validation, and call out to
    the in-memory WildDictionary to look it up.
    """
    self.data = self.request.recv(1024).strip()

    if len(self.data) > 15 or re.search('[^?A-Z]', self.data):
      return

    t0 = t_start = time.time()
    results = dictionary.lookup(self.data)
    lookup_time = time.time() - t0

    t0 = time.time()
    self.request.send('\n'.join(results) + '\n')
    network_time = time.time() - t0

    log.info('Handled request "%s" in %.3fs (%d results). '
             'lookup: %.3fs; network: %.3fs',
      self.data, time.time() - t_start, len(results),
      lookup_time, network_time)


# Create a threaded TCP server class per the SocketServer docs.
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
  pass

if __name__ == "__main__":
  # Setup some pretty logging.
  log = logging.getLogger('wild_server')
  log.setLevel(logging.INFO)
  handler = logging.StreamHandler(sys.stdout)
  handler.setFormatter(
  logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
  log.addHandler(handler)

  if len(sys.argv) != 4:
    print 'usage: wild_server.py <dictionary_file> <host> <port>'
    print '  e.g. wild_server.py my_dictionary localhost 9999'
    sys.exit(1)

  log.info('Initializing dictionary')
  dictionary = WildDictionary(sys.argv[1])

  log.info('Initializing server')
  address = (sys.argv[2], int(sys.argv[3]))
  server = ThreadedTCPServer(address, WildHandler)
  server.allow_reuse_address = True
  server.request_queue_size = 20
  server_thread = threading.Thread(target=server.serve_forever)
  server_thread.setDaemon(True)
  server_thread.start()
  log.info('Ready')
  while(True):
    time.sleep(60)
