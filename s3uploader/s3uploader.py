
import sys
import mimetypes

from ConfigParser import SafeConfigParser
from optparse import OptionParser
from boto.s3.connection import VHostCallingFormat
from boto.s3.connection import S3Connection
from boto.s3.key import Key

#Put your keys in awskeys.py: ACCESS_KEY, PASS_KEY
#chmod to 400 and put 'em in .gitignore :)
from awskeys import ACCESS_KEY, PASS_KEY

def uploadFile(bucket, filename):
    conn = S3Connection(ACCESS_KEY, PASS_KEY)
    b = conn.create_bucket(bucket)
    mime = mimetypes.guess_type(filename)[0]
    k = Key(b)
    k.key = filename
    k.set_metadata("Content-Type", mime)
    k.set_contents_from_filename(filename)
    k.set_acl("public-read")


def main():
    parser = OptionParser()
    parser.add_option("-b", "--bucket", dest="bucket", default="hotbuffer", help="s3 bucket name!")
    parser.add_option("-f", "--file", dest="filename", default="", help="filename")
    parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help="enable debugging")
    (options, args) = parser.parse_args()

    bucket = options.bucket
    debug = options.debug
    filename = options.filename

    if filename != "":
        uploadFile(bucket, filename)
    else:
        print "Yo dawg, you forget to put some file in ya bucket man..."

if __name__ == '__main__':
    main()
