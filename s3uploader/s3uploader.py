#!/usr/bin/python
import sys
import mimetypes

from ConfigParser import SafeConfigParser
from optparse import OptionParser
from boto.s3.connection import VHostCallingFormat
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from awskeys import ACCESS_KEY, PASS_KEY

def uploadFile(bucket, filename, mime=""):
    conn = S3Connection(ACCESS_KEY, PASS_KEY)
    b = conn.create_bucket(bucket)
    if mime == "":
        mime = mimetypes.guess_type(filename)[0]
        if mime == "":
            print "No default mime set, please use -m in args"
            return
    print "Uploading file %s of mimetype %s" % (filename, mime)
    k = Key(b)
    k.key = filename
    k.set_metadata("Content-Type", mime)
    k.set_contents_from_filename(filename)
    k.set_acl("public-read")

def main():
    parser = OptionParser()
    parser.add_option("-b", "--bucket", dest="bucket", default="hotbuffer", help="s3 bucket name!")
    parser.add_option("-f", "--file", dest="filename", default="", help="filename")
    parser.add_option("-m", "--mime", dest="mime", default="", help="set mimetype")
    (options, args) = parser.parse_args()

    bucket = options.bucket
    mime = options.mime
    filename = options.filename

    print "Uploading in bucket:", bucket
    if filename != "":
        uploadFile(bucket, filename, mime)
    else:
        print "Yo dawg, you forget to put some file in ya bucket man..."

if __name__ == '__main__':
    main()
