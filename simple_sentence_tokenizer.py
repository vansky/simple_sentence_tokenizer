## python3 simple_sentence_tokenizer.py --input INPUT_File --output OUTPUT_File
## cat INPUT_File | python3 simple_sentence_tokenizer.py > OUTPUT_File
# Outputs line-delimited sentences
# INPUT_File is a plain text file (defaults to stdout if --output missing or -)
# OUTPUT_File is when the output is stored (defaults to stdout if --output missing or -)

import re
import sys

OPTS = {}
for aix in range(1,len(sys.argv)):
  if len(sys.argv[aix]) < 2 or sys.argv[aix][:2] != '--':
    #filename or malformed arg
    continue
  elif aix < len(sys.argv) - 1 and len(sys.argv[aix+1]) > 2 and sys.argv[aix+1][:2] == '--':
    #missing filename
    OPTS[sys.argv[aix][2:1]] = True
  else:
    OPTS[sys.argv[aix][2:]] = sys.argv[aix+1]  

def hasInternalPunc(word):
  if repuncword.search(word) or word in exceptions:
    return(True)
  else:
    return(False)

reperiodendword = re.compile('[A-Za-z0-9]\.[\'"`]*$') #find word-final periods
reperiodinword = re.compile('[A-Za-z]\.[A-Za-z]') #find word-internal punc (e.g. acronyms)
repuncendword = re.compile('[A-Za-z0-9][\?!][\'"`]*$') #find word-final punc
recap = re.compile('[\'"`]*[A-Z]') #find caps

exceptions = ['mr','mrs','ms','dr','dra','sr','sra','st','rep','sen','gov','lt','gen','sgt','pvt','col','eg','ie','etc',\
                'jan','feb','mar','apr','jun','jul','aug','sep','sept','oct','nov','dec'] #these and all words with word-internal periods

nextwordexceptions = ['inc','co','corp','bros','ltd']

if 'input' in OPTS and OPTS['input'] != '-':
  with open(OPTS['input'], 'r') as f:
    text = f.readlines()
else:
  text = sys.stdin.readlines()

overix = 0 #ctr to track overall position in text

sentbounds = [0]
outtext = []

NUMLINES = len(text)
FIRST = True

for lix,line in enumerate(text):
  sline = line.strip().split()
  if sline == []:
    if not FIRST:
      #ensure we don't get trigger-happy about initial blank lines
      sentbounds.append(overix)
    continue
  FIRST = False
    
  for wix,word in enumerate(sline):
    #if there's non-period punctuation at the end of word (and we're not at the end of the file) OR
      #the word ends with a period AND the word isn't an exception AND the next word begins with a capital AND
      #the next word isn't a nextwordexception AND
      #the word has no internal periods AND the word is longer than 'X.' (to avoid middle initial confusion)
      # we assume sentences can't end with acronyms, which isn't true, but it's what we're assuming for now
    if (repuncendword.search(word) and (lix < NUMLINES - 1 or wix < len(sline) )) or \
          ( reperiodendword.search(word) and ''.join(word.lower().split('.')) not in exceptions and \
              (( wix < len(sline)-1 and recap.match(sline[wix+1])) or \
                 (wix == len(sline)-1 and lix < NUMLINES - 1 and text[lix+1].strip().split() != [] and recap.match(text[lix+1].strip().split()[0]))) and \
              (( wix < len(sline)-1 and sline[wix+1].lower().strip(',.') not in nextwordexceptions) or \
                 (wix == len(sline)-1 and lix < NUMLINES - 1 and text[lix+1].strip().split() != [] and \
                    text[lix+1].strip().split()[0].lower().strip(',.') not in nextwordexceptions)) \
              and not reperiodinword.search(word) and len(word) > 2):
      sentbounds.append(overix + wix + 1) #if this is the end of a sentence, the NEXT ix is the beginning of a sentence
  overix += len(sline)
  outtext += sline

previx = 0
if 'output' in OPTS and OPTS['output'] != '-':
  with open(OPTS['output'],'w') as f:
    for s in sentbounds[1:]:
      output = ' '.join(outtext[previx:s])
      if output.strip() != '':
        f.write(output+'\n')
      previx = s
else:
  for s in sentbounds[1:]:
    output = ' '.join(outtext[previx:s])
    if output.strip() != '':
      sys.stdout.write(output+'\n')
    previx = s