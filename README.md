simple_sentence_tokenizer
=========================

Tool that organizes text as one sentence per line  

Useful for preparing sentences for parsing or for the Penn Tokenizer  

Some examples of how to run the script:  

    python simple_sentence_tokenizer.py --input INPUT_File --output OUTPUT_File  
    cat INPUT_File | python simple_sentence_tokenizer.py > OUTPUT_File  

INPUT_File is a plain text file (defaults to stdin if --input is - or is missing)  
OUTPUT_File is a file with one sentence per line (defaults to stdout if --output is - or is missing)  

The script will combine incomplete fragments to make a sentence and will split multiple sentences:

    Input:  
        ``The girl,'' she said,     
        ``ate the cake.''  
        The frog jumped over the dog. What a lazy dog!  
    Output:  
        ``The girl,'' she said, ``ate the cake.''  
        The frog jumped over the dog.  
        What a lazy dog!  

Compatible with both Python 2.x and Python 3.x
