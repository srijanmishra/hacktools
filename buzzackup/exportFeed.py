#!/usr/bin/env python
##############################################################################
# buzzackup - google buzz backup tool
# author: rohityadav, hack'd just before `rm buzz-account` ];] buzz s**ks
# notes: ain't elegant, just one night's hacking, enjoy!
# help: python buzzackup.py --help
###############################################################################

import xml.etree.ElementTree as ET
from django.utils.encoding import smart_str
from calendar import month_name
from common import readFeed, readFeedFromFile, namespace, namespace_thr, namespace_likers, apiPrefix, feedUrl, likeFeedUrl

def exportHtmlFeed(feedFile, directory, fileCount, htmlOutputFileName, handle, nick, reverse = False):
    f = open(htmlOutputFileName, 'w')
    f.write("<html><head><meta http-equiv=Content-Type content=\"text/html; charset=UTF-8\">")
    f.write("<link rel=\"stylesheet\" href=\"buzzout.css\" type=\"text/css\" media=\"screen\" />")
    f.write("<title>Buzzackup of %s<title></head><body>" % nick)

    data = readFeedFromFile(feedFile)
    entries = ET.XML(data).findall(namespace + "entry")
    if reverse: entries.reverse()
    
    f.write("<h1>Buzz by %s {%d}!</h1>" % (nick, len(entries)))
    entryNumber = 0
    print "Crawling Google network for buzz feeds... Found %d buzz posts for %s" % (len(entries), nick)

    for entry in entries:
        #Buzz post starts        
        f.write("<div class=\"buzz\">")
        
        #Process post date
        entryDate = entry.findall(namespace + 'updated')[0].text.split('T')[0].split('-')
        prettyDate = "%s %s %s " % (entryDate[2], month_name[int(entryDate[1])], entryDate[0])
        f.write("<strong>" + prettyDate + "</strong>")

        #Process post content
        post = entry.findall(namespace + 'content')[0].text
        f.write("<div class=\"post\">" + smart_str(post) + "</div>")

        #Process Like feed
        postId = entry.findall(namespace + 'id')[0].text
        likeFeed = likeFeedUrl % (handle, postId)
        rawLikedFeed = readFeed(likeFeed)
        likersTree = ET.XML(rawLikedFeed )
        print "Like Tree length", len(likersTree)
        totalLikes = likersTree.findall(namespace_likers + 'totalResults')[0].text
        likeCounter = 0
        if int(totalLikes) != 0:
            print "Hmm... [%s] likes on your post" % totalLikes
            f.write("<div style=\"color:#666;\" class=\"likers\">Liked by [%s]: " % totalLikes)
            likers = likersTree.findall(namespace_likers + 'entry')
            for liker in likers:
                likerName = liker.findall(namespace_likers + 'displayName')[0].text
                likerUri = liker.findall(namespace_likers + 'profileUrl')[0].text
                f.write("<a href=\"%s\">%s</a>" % (likerUri, smart_str(likerName)))
                likeCounter += 1
                if likeCounter != len(likers):
                    f.write(", ")
            f.write("</div>")
        
        links = entry.findall(namespace + 'link')
        f.write("<div class=\"links\">")

        for link in links:
            if link.get('rel') == 'enclosure':
                f.write("<a href=\"" + smart_str(link.get('href')) + "\">" + smart_str(link.get('title')) + "</a><br>")
            if link.get('rel') == 'http://schemas.google.com/buzz/2010#liked':
                totalLikes = likersTree.findall(namespace_likers + 'totalResults')[0].text
            if link.get('rel') == 'replies':
                replyCount = entry.findall(namespace_thr + 'total')[0].text
                if int(replyCount) != 0:
                    f.write("<div class=\"comments\">Comments(%s)<br>" % replyCount)
                    rawReplyFeed = readFeed(link.get('href')) 
                    comments = ET.XML(rawReplyFeed).findall(namespace + 'entry')
                    for comment in comments:
                        f.write("<div style=\"margin-left:30px;\" class=\"comment\">")
                        reply = comment.findall(namespace + 'content')[0].text
                        author = comment.findall(namespace + 'author')[0]
                        authorName = author.findall(namespace + 'name')[0].text
                        authorUri = author.findall(namespace + 'uri')[0].text
                        commentDate = entry.findall(namespace + 'updated')[0].text.split('T')[0].split('-')
                        prettyDate = "%s %s %s " % (commentDate[2], month_name[int(commentDate[1])], commentDate[0])
                        f.write("<a href=\"%s\">%s</a> (%s) - %s" % (authorUri, smart_str(authorName), prettyDate, smart_str(reply)))
                        f.write("</div>")
                    f.write("</div>")
        f.write("</div></div><br>")
        entryNumber += 1
        print "Processing buzz post. Progress: (%d/%d) %d%%" % (entryNumber, len(entries), entryNumber * 100 / len(entries))
        
    f.write('</body></html>')
    f.close()

    print "Exported to HTML output:", htmlOutputFileName
    
def testmain():
    handle = 'rohityadav89'
    nick = 'Test Buzzackup'

    fileName = "buzzackup.xml"
    htmlOutputFileName = "buzzout-%s.html" % handle
    exportHtmlFeed(fileName, "./", 0, htmlOutputFileName, handle, nick)

if __name__ == '__main__':
    testmain()
