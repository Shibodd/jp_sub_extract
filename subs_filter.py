import lib.subs_tokenizer as subs_tokenizer
import lib.jmdict_whitelist as jmdict_whitelist

import pathlib

def get_whitelist(jmdict_path, whitelist_pickle_path = None):
  """
  Unpickles the whitelist from whitelist_pickle_path if it is not None and the file exists;
  
  otherwise, it generates a whitelist by parsing the JMdict file at jmdict_path,
  pickles the result into whitelist_pickle_path, and returns the whitelist.
  """

  if whitelist_pickle_path is not None:
    import pickle

  if isinstance(whitelist_pickle_path, str):
    whitelist_pickle_path = pathlib.Path(whitelist_pickle_path)

  if whitelist_pickle_path is None or not whitelist_pickle_path.exists():

    print("Generating whitelist from dictionary...")
    whitelist = set(jmdict_whitelist.get_whitelist(str(jmdict_path)))

    if whitelist_pickle_path is not None:
      with whitelist_pickle_path.open('wb+') as file:
        print("Pickling whitelist...")
        pickle.dump(whitelist, file)
    
    return whitelist
    
  else:
    print("Loading pickled whitelist...")

    with whitelist_pickle_path.open('rb') as file:
      ans = pickle.load(file)
      return ans
    
def write_filtered_subs(whitelist: set, subs_path, output_path, sudachi_dict_type = 'full'):
  """
  Reads, tokenizes and filters the subs_path .srt file,
  then outputs the result into output_path.
  """

  if isinstance(subs_path, str):
    subs_path = pathlib.Path(subs_path)

  if isinstance(output_path, str):
    output_path = pathlib.Path(output_path)

  tokens = subs_tokenizer.tokenize_subs(str(subs_path), sudachi_dict_type=sudachi_dict_type)
  
  print("Filtering subs...")
  unique_words = set((tok for tok in tokens if tok in whitelist))

  print(f"Writing {len(unique_words)} unique words to {str(output_path)}...")

  with output_path.open('wt', encoding='utf8') as out:
    for word in unique_words:
      out.write(word + "\n")


if __name__ == "__main__":
  import argparse

  args = argparse.ArgumentParser()
  args.add_argument('srt_in',
                    help='The input .srt file.')
  
  args.add_argument('-o', default='out.txt', required = True,
                    help='A file in which the filtered words will be stored.')
  
  args.add_argument('--jmdict', default='JMdict_e', required = True,
                    help='The path to the JMdict file')
  
  args.add_argument('--sudachi_dict_type', default='full', required = True, 
                    help='Either small, core, full, depending on the sudachidict version you installed.')
  
  args.add_argument('--whitelist_cache', required = False,
                    help='Where to store the cached whitelist.')
  
  args = args.parse_args()

  whitelist = get_whitelist(args.jmdict, args.whitelist_cache)
  write_filtered_subs(whitelist, args.srt_in, args.o, args.sudachi_dict_type)
  