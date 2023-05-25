import lxml.etree

def elem_to_dict(element):
  """
  Recursively converts an lxml.etree._Element to a dictionary.
  Elements cannot have both text and children at the same time:
  in this case this raises an Exception.
  This is because if it didn't, one of the two would have to be silently discarded.
  """

  text = element.text
  if text is not None:
    text = text.strip()
    if len(text) == 0:
      text = None

  if len(element) == 0:
    return text
  else:
    if text is not None:
      raise Exception("Content and children found at the same time!")

    ans = {}
    ents = []

    for child in element:
      if isinstance(child, lxml.etree._Entity):
        # Entity references are returned as children of elements
        ents.append(child.name)
      else:
        tag = child.tag
        child_dict = elem_to_dict(child)
        child_is_list = isinstance(child_dict, list)

        if tag in ans:
          if child_is_list:
            ans[tag].extend(child_dict)
          else:
            ans[tag].append(child_dict)
        else:
          if child_is_list:
            ans[tag] = child_dict
          else:
            ans[tag] = [ child_dict ]

    if len(ents) > 0:
      if len(ans) > 0:
        raise Exception("Content and children found at the same time!")
      ans = ents
      
    return ans

def parse_xml(source, tag, **kwargs):
  for ev, elem in lxml.etree.iterparse(source, tag=tag, resolve_entities = False):
    yield elem_to_dict(elem)
    elem.clear()