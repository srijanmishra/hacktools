#!/usr/bin/env python
##############################################################################
# buzzackup - google buzz backup tool
# author: rohityadav, hack'd just before `rm buzz-account` ];] buzz s**ks
# notes: ain't elegant, just one night's hacking, enjoy!
# help: python buzzackup.py --help
###############################################################################

from buzzackup.importFeed import importBuzzFeed
from buzzackup.exportFeed import exportHtmlFeed
    
def main():
    parser = OptionParser()
    parser.add_option("-p", "--profile", dest="handle", default="rohityadav89", help="Your Google Buzz Profile id/handle")
    parser.add_option("-n", "--name", dest="nick", default="Rohit Yadav", help="Your Name")
    parser.add_option("-f",, dest="fileName", default="", help="Specify a xml feed file as input")
    parser.add_option("-fn", "--feedfileno", dest="fileName", default=0, help="Specify a xml feed file as input")

    parser.add_option("-d", dest="download", action="store_true", default=False, help="Enable to fetch the feed. Default to use fetched file.")
    parser.add_option("-e", dest="export", action="store_true", default=False, help="Enable to parse a pre-fetched xml feed file.")
    (options, args) = parser.parse_args()

    handle = options.handle
    nick = options.nick
    if options.fileName == "":
        fileName = "buzzackup-%s-%s.xml" % (handle, '%d')

    if options.download:
        (totalFiles, totalEntries) = importBuzzFeed(handle, fileName, feedUrl % handle)
        print "Buzz feed backedup in %d files, total posts found are: %d" % (totalFiles, totalEntries)

    if options.export:
        htmlOutputFileName = "buzzout-%s.html" % handle
        exportHtmlFeed(fileName, htmlOutputFileName, handle, nick)

if __name__ == '__main__':
    main()
