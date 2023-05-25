# jp_sub_extract

Extracts Japanese words from an .srt subtitles file, filters them using the JMdict and then outputs the result into an output file.
Not available as a pip package.

Prerequisites:
Python 3, and the following pip packages (note that you can choose the sudachidict-* version between small, core, full: read https://github.com/WorksApplications/SudachiPy#dictionary-edition for details):
```
pip install lxml
pip install srt
pip install sudachipy
pip install sudachidict-core
```

You also need a JMdict edition, which you can download from https://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project

Example usage:

```bash
python3 subs_filter.py \
-i subs.srt \
-o out.txt \
--jmdict JMdict_e \
--sudachi_dict_type core \
--whitelist_cache whitelist.pickle
```

Where:
`-i` is the input .srt file;
`-o` is the output file;
`--jmdict` is the JMdict file;
`--sudachi_dict_type` is the sudachidict version you installed;
`--whitelist_cache` is, if you want to cache the whitelist, where it will be pickled and depickled.

If you want to change the filter code, it is located in lib/jmdict_whitelist.py.
