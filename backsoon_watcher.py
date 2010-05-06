#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# 爆寸砲
# クパチーノ方面に祈れ！
#

import os
import sys
import time
import urllib2
from optparse import OptionParser

try:
    import Growl
    GROWL_ENABLED = True
except ImportError:
    GROWL_ENABLED = False

DEFAULT_URL = 'http://store.apple.com/jp'

def main():
    usage = 'usage: %s [options] URL' % os.path.basename(__file__)
    p = OptionParser(usage=usage)
    p.add_option('-n', '--interval', type='float', default=5.0, metavar='<seconds>', help='seconds to wait between updates')
    opts, args = p.parse_args()
    if not args:
        url = DEFAULT_URL
    else:
        url = args[0]
    watch(url, opts.interval)

def watch(url, interval):
    base = None
    tries = 0
    while True:
        if base:
            try:
                tries += 1
                current = http_get(url)
                if current != base:
                    notify()
                    break
                sys.stdout.write("tries: %d\r" % tries)
                sys.stdout.flush()
            except StandardError, e:
                print e
                print 'An error accurred. but continue to watch anyway...'
        else:
            base = http_get(url)
            print 'url: %s, size: %d byte' % (url, len(base))
        time.sleep(interval)

def http_get(url):
    return urllib2.urlopen(url).read()

def notify():
    print 'Apple Store is Now Live!!!'
    notify_growl()

def notify_growl():
    if not GROWL_ENABLED: return
    g = Growl.GrowlNotifier(
        applicationName=os.path.basename(__file__),
        notifications=['Live'])
    g.register()
    g.notify(
        noteType='Live',
        title='Apple Store is Now Live',
        description=u'開いた！！！',
        sticky=True)


if __name__ == '__main__':
    main()


