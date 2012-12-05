"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
# Import helpers as desired, or define your own, ie:
# from webhelpers.html.tags import checkbox, password

import datetime
from webhelpers import util,html
from webhelpers.html import tags
import re

def format_time(seconds):
    try:
        seconds = int(seconds)
        hours = seconds / 60 / 60
        minutes = (seconds - hours * 60 * 60) / 60
        seconds = seconds - (hours * 60 * 60) - (minutes * 60)
        if hours:
            return "%d:%d:%02d" % (hours,minutes,seconds)
        else:
            return "%d:%02d" % (minutes,seconds)
    except TypeError:
        return '00:00'

def format_track_time(track):
    try:
        seconds = track['time']
        return format_time(seconds)
    except KeyError:
        return '00:00'

def format_filesize(bytes):        
    kb = "%02.2fKB" % (bytes / 1024.0)
    return kb

def escape_js(s):
    s = re.sub(r'\\', r'\\\\', (s or ''))
    s = re.sub(r'\r\n|\n|\r', r'\\n', s)
    s = re.sub(r'(["\'])', r'\\\1', s)
    return s

def timestamp_to_friendly_date(ts):
    try:
        date = datetime.datetime.fromtimestamp(int(ts))
        return date.strftime("%Y-%m-%d %H:%M:%S")
    except TypeError:
        return 'unable to determine'

def format_title(t,trackno=None):
    try:
        t['formattedtrack'] = u"%02d. %s" % (int(t['track']),t['title'])
    except KeyError,e:
        if 'title' in t:
            t['formattedtrack'] = u"%s" % (t['title'])
    except ValueError,e:
        if 'title' in  t:
            t['formattedtrack'] = u"%s. %s" % (t['track'],t['title'])
        else:
            if 'title' in t:
                t['formattedtrack'] = u"%s" % t['title']
    
    if not 'formattedtrack' in t:
        if trackno:
            t['formattedtrack'] = u"%d." % trackno
        else:
            t['formattedtrack'] = u'<unknown>'

def format_title_search(t):
    try:
        t['formattedtrack'] = u"%s - %s - %s" % (t['artist'],t['album'],t['title'])
    except KeyError,e:
        if 'title' in t:
            t['formattedtrack'] = u"%s" % (t['title'])
    
    if not 'formattedtrack' in t:
        t['formattedtrack'] = u"%s" % t['file']
