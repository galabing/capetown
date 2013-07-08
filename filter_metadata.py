#!/usr/bin/python2.7

""" Reads the downloaded metadata, applies filtering on the items
    (eg, with license constraints), and outputs a list of urls for
    downloading the large-size photos that are not filtered out.
    The photos can be downloaded by 'wget -i <url_file>'.
"""

import optparse

ITEM_HEADER = 'id : '
DELIMITER = ' : '
# See http://www.flickr.com/services/api/flickr.photos.licenses.getInfo.html
VALID_LICENSES = set(['1', '2', '4', '5'])
MIN_ACCURACY = 15

def parse_next(metadata_fp):
  while True:
    line = metadata_fp.readline()
    if line == '': break
    if line.startswith(ITEM_HEADER): break
  if line == '': return None
  assert line.startswith(ITEM_HEADER)
  item = dict()
  idk, idv = line[:-1].split(DELIMITER)
  item[idk] = idv
  while True:
    line = metadata_fp.readline()
    if line == '' or line == '\n': break
    line = line[:-1]
    d = line.find(DELIMITER)
    assert d > 0
    k = line[:d]
    v = line[d+len(DELIMITER):]
    item[k] = v
  return item

def keep(item):
  if item['license'] not in VALID_LICENSES: return False
  if int(item['accuracy']) < MIN_ACCURACY: return False
  return True

def make_url(item):
  return 'http://farm%s.staticflickr.com/%s/%s_%s_b.jpg' % (
      item['farm'], item['server'], item['id'], item['secret'])

def filter_all(metadata_fp):
  urls = []
  while True:
    item = parse_next(metadata_fp)
    if item is None: break
    if not keep(item): continue
    urls.append(make_url(item))
  return urls

def main():
  parser = optparse.OptionParser()
  parser.add_option('--metadata_file')
  parser.add_option('--url_file')
  options, args = parser.parse_args()
  if not options.metadata_file or not options.url_file:
    parser.error('Must specify --metadata_file, --url_file')

  with open(options.metadata_file, 'r') as fp:
    urls = filter_all(fp)
  with open(options.url_file, 'w') as fp:
    for url in urls:
      print >> fp, url

if __name__ == '__main__':
  main()

