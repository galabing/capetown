#!/usr/bin/python2.7

import flickrapi
import optparse
from time import sleep

API_KEY = '54556789832f474d217e6c30ef2223b7'
MAX_TAKEN_DATE = '1969-12-31'
HAS_GEO = '1'
# TODO: For now 'description' is left out, so are url_* except for url_l
# The missing url_* can probably be reconstructed by appending appropriate
# suffixes to the base url. This list should be refined.
EXTRAS = ('license,date_upload,date_taken,owner_name,icon_server'
          ',original_format,last_update,geo,tags,machine_tags,o_dims,views'
          ',media,path_alias,url_l')
PER_PAGE = '500'
# TODO: This is useful for tests. Make it a flag.
MAX_ITEMS = 1000
SLEEP_SECS = 1.0

# The list of fields should be in sync with the EXTRAS above.
# Note that some items in EXTRAS lead to more than one fields.
# TODO: Some fields are probably not needed.
FIELDS = [
    'id', 'owner', 'secret', 'server', 'farm', 'title', 'ispublic', 'isfriend',
    'isfamily', 'license', 'dateupload', 'datetaken', 'datetakengranularity',
    'ownername', 'iconserver', 'iconfarm', 'originalsecret', 'originalformat',
    'lastupdate', 'latitude', 'longitude', 'accuracy', 'context', 'place_id',
    'woeid', 'geo_is_family', 'geo_is_friend', 'geo_is_contact',
    'geo_is_public', 'tags', 'machine_tags', 'o_width', 'o_height', 'views',
    'media', 'media_status', 'pathalias', 'url_l'
]

logger = None

def print_header(metadata_fp):
  # Note: These should be in sync with the constants defined above.
  print >> metadata_fp, '# MAX_TAKEN_DATE = %s' % MAX_TAKEN_DATE
  print >> metadata_fp, '# HAS_GEO = %s' % HAS_GEO
  print >> metadata_fp, '# EXTRAS = %s' % EXTRAS
  print >> metadata_fp, '# PER_PAGE = %s' % PER_PAGE
  print >> metadata_fp, '# MAX_ITEMS = %d' % MAX_ITEMS
  print >> metadata_fp, '# SLEEP_SECS = %f' % SLEEP_SECS
  print >> metadata_fp, '# FIELDS = %s' % ','.join(FIELDS)
  print >> metadata_fp

def print_item(metadata_fp, item):
  pass

def download_page(metadata_fp, flickr, page, ids):
  return 0

def download_all(metadata_fp):
  print_header(metadata_fp)
  flickr = flickrapi.FlickrAPI(API_KEY)
  page = 1
  ids = set()
  while True:
    pages = download_page(metadata_fp, flickr, page, ids)
    if page >= pages: break
    page += 1
  return ids

def main():
  parser = optparse.OptionParser()
  parser.add_option('--metadata_file')
  parser.add_option('--verbose', action='store_true')
  options, args = parser.parse_args()
  if not options.metadata_file:
    parser.error('Must specify --metadata_file')

  with open(options.metadata_file, 'w') as fp:
    ids = download_all(fp)
    print 'Downloaded %d items' % len(ids)

if __name__ == '__main__':
  main()

