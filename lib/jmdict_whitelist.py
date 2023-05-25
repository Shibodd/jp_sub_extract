import itertools
def whitelist_predicate(entry):
  POS_PREFIX_WHITELIST = [ 'v', 'adj', 'n', 'iv', 'adv' ]

  pos = itertools.chain.from_iterable(x.get('pos') for x in entry.get('sense', tuple()))

  return any(
    any((x.startswith(prefix) for prefix in POS_PREFIX_WHITELIST)) 
    for x in pos 
  )

import pprint
def whitelist_projection(entry):
  ans = itertools.chain.from_iterable(
    k_ele.get('keb', tuple())
    for k_ele in entry.get('k_ele', tuple())
  )

  """
  Too ambiguous.

  readings = itertools.chain.from_iterable(
    r_ele.get('reb', tuple())
    for r_ele in entry.get('r_ele', tuple())
  )
  ans = itertools.chain(readings, ans)
  """

  return tuple(ans)

import lib.xml_parse_elems as xml_parse_elems

def get_whitelist(dict_file):
  return itertools.chain.from_iterable(
    whitelist_projection(entry) 
    for entry in xml_parse_elems.parse_xml(dict_file, 'entry') 
    if whitelist_predicate(entry)
  )