#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# 爆寸砲
# クパチーノ方面に祈れ！
#

import os
import sys
import time
import subprocess
import urllib2
import difflib
from optparse import OptionParser

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
    notify()
    print_diff(base, current)
    open_url_by_browser(url)

def http_get(url):
    try:
        return urllib2.urlopen(url).read()
    except urllib2.HTTPError, e:
        if e.code == 404:
            return e.read()
        raise e

def notify():
    print 'Apple Store is Now Live!!!'
    notify_say()
    notify_growl()

def notify_say():
    cmd = '/usr/bin/say Apple Store is Now Live!'
    subprocess.Popen(cmd, shell=True)

def notify_growl():
    try:
        import Glowl
    except ImportError:
        return
    g = Growl.GrowlNotifier(
        applicationName=os.path.basename(__file__),
        notifications=['Live'])
    g.register()
    g.notify(
        noteType='Live',
        title='Apple Store is Now Live',
        description=u'開いた！！！',
        sticky=True)

def open_url_by_browser(url):
    cmd = '/usr/bin/open %s' % url
    subprocess.Popen(cmd, shell=True)

def print_diff(base, current):
    for buf in difflib.unified_diff(
            base.splitlines(),
            current.splitlines()):
        print buf


if __name__ == '__main__':
    main()


