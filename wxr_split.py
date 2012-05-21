"""
This program is for splitting a single giant Wordpress WXR file into
multiple smaller WXR files to get around common file upload size
limits.
"""

__author__ = 'John Wiseman <jjwiseman@gmail.com>'

import argparse
import operator
from xml.etree import ElementTree


# 2 MB is a common file size limit, aim for 90% of that just to be
# safe.

DEFAULT_MAX_FILE_SIZE = int(1024 * 1024 * 1.8)

# We need to tell the ElementTree API what prefixes to use for each
# namespace or when we serialize to an XML string it will generate
# something dumb like
#
# <rss version="2.0"
#     xmlns:ns0="http://wordpress.org/export//excerpt/"
#     xmlns:ns1="http://purl.org/rss/1.0/modules/content/"
# >
#
# even if the original document uses nice namespace prefixes like
# xmlns:excerpt, xmlns:content, etc.

NAMESPACES = {
  'excerpt': 'http://wordpress.org/export//excerpt/',
  'content': 'http://purl.org/rss/1.0/modules/content/',
  'wfw': 'http://wellformedweb.org/CommentAPI/',
  'dc': 'http://purl.org/dc/elements/1.1/',
  'wp': 'http://wordpress.org/export//',
  }


def split_file(input_file, max_file_size):
  """Splits a single WXR file into multiple, smaller files.

  Arguments:
    input_file(str): The path of the WXR file to split.
    max_file_size(int): The maximum size of each partial file.
  """
  for prefix in NAMESPACES:
    ElementTree.register_namespace(prefix, NAMESPACES[prefix])
  print 'Parsing...'
  root = ElementTree.parse(input_file).getroot()
  channel = root.find('channel')
  items = channel.findall('item')
  print 'Found %s items' % (len(items),)
  remove_items(channel, items)

  partial_count = 1
  first_items, rest_items = partition_items(
    root, items, max_file_size)
  while first_items:
    add_items(channel, first_items)
    xml = ElementTree.tostring(root)
    partial_filename = compute_partial_filename(input_file, partial_count)
    print 'Writing %s with %s items (%s bytes, %.2f%%)' % (
      partial_filename, len(first_items), len(xml),
      100.0 * len(xml) / max_file_size)
    with open(partial_filename, 'wb') as out:
      out.write(xml)
    partial_count += 1
    first_items, rest_items = partition_items(
      root, rest_items, max_file_size)


# Too bad the standard Python version of this function from the bisect
# module isn't general purpose.

def bisect_left(a, x, lo=0, hi=None, key_fn=None):
  """Return the index where to insert item x in list a, assuming a is
  sorted.

  The return value i is such that all e in a[:i] have e < x, and all e
  in a[i:] have e >= x.  So if x already appears in the list,
  a.insert(x) will insert just before the leftmost x already there.

  Optional args lo (default 0) and hi (default len(a)) bound the slice
  of a to be searched.
  """
  if not key_fn:
    key_fn = operator.getitem
  if lo < 0:
    raise ValueError('lo must be non-negative')
  if hi is None:
    hi = len(a)
  while lo < hi:
    mid = (lo + hi) // 2
    if key_fn(a, mid) < x:
      lo = mid + 1
    else:
      hi = mid
  return lo


def partition_items(root, items, max_file_size):
  """Finds the initial subsequence of items such that if that
  subsequence is serialized to XML the file size would be less than
  but as close as possible to max_file_size.

  Returns:
    A tuple (FIRST, REST) where FIRST is the initial subsequence of
    items that will fit in the specified size and REST is the rest of
    the items.
  """

  def file_size(items, pos):
    add_items(channel, items[0:pos])
    size = len(ElementTree.tostring(root))
    remove_items(channel, items[0:pos])
    return size

  channel = root.find('channel')
  remove_items(channel, channel.findall('item'))
  if items:
    partition_idx = bisect_left(items, max_file_size, key_fn=file_size)
    partition_idx -= 1
    first_items = items[0:partition_idx]
    rest_items = items[partition_idx:]
    return first_items, rest_items
  else:
    return [], []


def add_items(element, items):
  for item in items:
    element.append(item)


def remove_items(element, items):
  for item in items:
    element.remove(item)


def compute_partial_filename(path, n):
  dot_pos = path.rfind('.')
  if dot_pos >= 0:
    return '%s-%s%s' % (path[0:dot_pos], n, path[dot_pos:])
  else:
    return '%s-%s' % (path, n)


def main():
  parser = argparse.ArgumentParser(
    description='Split one large WXR file into multiple smaller files.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('input_file', metavar='PATH',
                      help='Path of the input WXR file')
  parser.add_argument('--max_size', dest='max_size', type=int,
                      default=DEFAULT_MAX_FILE_SIZE,
                      help='The maximum size of output files.')
  args = parser.parse_args()
  split_file(args.input_file, args.max_size)


if __name__ == '__main__':
  main()
