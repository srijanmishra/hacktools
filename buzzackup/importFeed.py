#!/usr/bin/env python
##############################################################################
# buzzackup - google buzz backup tool
# author: rohityadav, hack'd just before `rm buzz-account` ];] buzz s**ks
# notes: ain't elegant, just one night's hacking, enjoy!
# help: python buzzackup.py --help
###############################################################################

import urllib2
import xml.etree.ElementTree as ET
from ConfigParser import SafeConfigParser
from optparse import OptionParser
from django.utils.encoding import smart_str
from calendar import month_name

namespace = "{http://www.w3.org/2005/Atom}"
namespace_thr = "{http://purl.org/syndication/thread/1.0}"
namespace_likers = "{http://portablecontacts.net/ns/1.0}"
apiPrefix = "http://www.googleapis.com/buzz/v1/"
feedUrl = apiPrefix + "activities/%s/@public?max-results=100&bhu"

def readFeed(url):
    if url != None:
        request = urllib2.Request(url);
        response = urllib2.urlopen(request)
        rawFeed = response.read()
        return rawFeed
    return None

def readFeedFromFile(fileName = 'buzzackup.xml'):
    f = open(fileName, 'r')
    data = f.read()
    f.close()
    return data

def importBuzzFeed(handle, fileName, url, stock = 0):
    print "Getting raw Google Buzz feed from:", url
    f = open(fileName % stock, 'w')
    rawFeed = readFeed(url);
    f.write(rawFeed)
    f.close()
    print "Raw feed saved as file: %s" % (fileName % stock)
    
    tree = ET.XML(rawFeed)
    links = tree.findall(namespace + "link")

    totalFiles = 1
    totalEntries = len(tree.findall(namespace + "entry"))
    recFiles = 0
    recEntries = 0

    for link in links:
        if link.get('rel') == 'next':
            (recFiles, recEntries) = importBuzzFeed(handle, fileName, 'http' + link.get('href')[5:]+'&ampbhu', stock + 1)
    return (totalFiles+recFiles, totalEntries+recEntries) 
  
def testmain():    
    handle = 'rohityadav89'
    nick = 'Rohit Yadav'

    fileName = "buzzackup-%s-%s.xml" % (handle, '%d')

    (totalFiles, totalEntries) = importBuzzFeed(handle, fileName, feedUrl % handle)
    print "Buzz feed backedup in %d files, total posts found are: %d" % (totalFiles, totalEntries)

if __name__ == '__main__':
    testmain()
