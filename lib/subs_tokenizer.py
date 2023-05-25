import srt
import sudachipy
import sudachipy.dictionary

def read_subs(file):
  with open(file, "r", encoding = "utf8") as f:
    for sub in srt.parse(f):
      yield sub.content

def tokenize_subs(
    file, 
    sudachi_dict_type = 'full', 
    sudachi_split_mode = sudachipy.SplitMode.B):
  
  tokenizer_obj = sudachipy.dictionary.Dictionary(dict_type=sudachi_dict_type).create(mode=sudachi_split_mode)
  for line in read_subs(file):
    for tok in tokenizer_obj.tokenize(line):
      yield tok.dictionary_form()