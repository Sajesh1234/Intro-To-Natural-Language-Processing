"""
PA 2 - N-Gram Language Model
Sajesh Sahoo
2-19-2024
CMSC 416

1. Create a Program that will create randomly generated sentences from sources provided by the user,
through the commandline arguments. it takes the books it calculates the probablity of words being next to each other,
and based on that it generated sentences.
2. To run the program: have the text files in the same directory as this program, to run it open the command promt,
go to the directory by typing cd (name of directory). and then type the following command into the command line:

ngram.py n m input-file/s

n is the number of previous words taken into consideration when generating the sentence, so the higher the number 'n',
the more organized the sentence will be.

m is the number of senteces you want to generate through this program.

the input-files, are the traning materials that are needed for this program to work, u have to supply at least one for this
program to be able to generate sentences.

Examples of the Program using "Introduction to Sally" by Elizabeth Von Arnim and "The tower" by W. B. Yeats
--> python ngram.py 3 10 pg72979.txt pg72985.txt
1:Now he too had played as sally put it off for another day and night while she was moulding him into the dark shut out
2:We re outside---- hastily he looked at him and sally
3:Pinner in false positions
4:Yes; see what indeed
5:Quite perfect he said
6:It wouldn t let her do anything sooner than-- she looked at her very much like the sword
7:I like that said mr
8:Pinner--and there was no place for her to sit there quietly and know whatever flourish and decline these stones remain their monument and mine
9:It really isn t seriously disputing it said charles quickly eager to get them cut and sew be neat in everything in the watches of the wrong sort but the part that clusters round the corner
10:What does one do to a vivid sense of mr

3. The program first takes in the arguments provided by the user in the command line. second it creates ngrams based on the users input.
it is then cleaned and tokenized, and then zipped to be returned as a list. if the n is 1 then it called the uni function which is designed for 1-grams,
as markovs assumption cannot be applied to it. to generate senteces for multiple n-grams we use sentence function which then calculates the probablity of
each word, using the overall frequency of each word. and then lastly, the create_sen creates the sentences for the n-grams. 
"""
import sys
import re
import random

# Convert Lists to Strings. 
def listToString(s):
    str1 = " "
    return str1.join(s)

# Create N-grams from text
def create_ngram(text, n):
    # Preprocess and clean the input. 
    text = text.lower()
    text = re.sub(r"['\"“”‘’„”«»,]", ' ', text)
    text = re.sub(r"\n", " ", text)
    
    # Adding Start and End Tags. 
    start = ""
    for i in range(n - 1):
        start = start + " <start> "  
    text = start + text
    start = " <end> " + start

    # Replacing Punctuation with Start tags. 
    text = text.replace(".", start)
    text = text.replace("...", start)
    text = text.replace("....", start)
    text = text.replace("!", start)
    text = text.replace("?", start)
    text = text.replace("***", start)
    text = re.sub(r"  ", ' ', text)

    # Tokenizing texts. 
    tokenized = [token for token in text.split(" ") if token != ""]
    raw_tokens = [tokenized[i:] for i in range(0, n)]

    # https://stackoverflow.com/questions/66203861/how-is-does-zip-generate-n-grams
    ngrams = zip(*raw_tokens)
    return [" ".join(ngram) for ngram in ngrams]

# Goes through lists and returns the frequent distribution of words before them. 
def numerator(ngrams, n):
    freq_dist = {}
    
    for i in range(0, len(ngrams)):
        word = str(ngrams[i].split()[n - 1])
        #h is the context for the words, so previous words. 
        h = listToString(ngrams[i].split()[:(n - 1)])
        # Increase frequence of h if h already exists. 
        if h in freq_dist:
            if word in freq_dist[h]:
                freq_dist[h][word] += 1
            else:
                freq_dist[h][word] = {}
                freq_dist[h][word] = 1
                
        # If h does not exist, initialize it and set to 1
        else:
            freq_dist[h] = {}
            freq_dist[h][word] = {}
            freq_dist[h][word] = 1

    return freq_dist

def denominator(ngrams, n):
    freq_dist = {}

    for i in range(0, len(ngrams)):
        w = str(ngrams[i].split()[n - 1])
        h = listToString(ngrams[i].split()[:(n - 1)])
        # Increment frequency of h if context already exists in freq_dist
        if h in freq_dist:
            freq_dist[h] += 1
        # If h does not exist, initialize it and set to 1
        else:
            freq_dist[h] = {}
            freq_dist[h] = 1
    return freq_dist
    
# Function to generate unigrams since Markovs assumpstion does not apply to it.
def uni(sum_words, freq_words):
    sentence = ""
    ngram_arr = [" "]
    d = sum_words
    # Run until the <end> is reached. 
    while "<end>" not in ngram_arr:
        total = 0
        rand_num = random.uniform(0, 1)
        for word in freq_words:
            prob = freq_words[word] / d
            total += prob
            if rand_num < total:
                sentence = sentence + ngram_arr.pop(0) + " "
                ngram_arr.append(word)

                if "<end>" in ngram_arr:
                   sentence += " ".join(ngram_arr)
                break
    sentence = sentence.replace(" <end>", ".")

    
    return sentence.capitalize().rstrip()

#function to create sentences, it calcualtes the probablity based on the previous word
#and it uses a random number to pick the next words in the sentence. .
def sentence(freq_num, freq_den, n):
    sentence = ""
    ngram_arr = []

    # Initialize n-1 grams with start tags
    for o in range(n - 1):
        ngram_arr.append("<start>")

    while "<end>" not in ngram_arr:
        h = " ".join(ngram_arr)
        # Is used to handle missing words
        freq_word = freq_num.get(h, {})
        sum_prob = 0
        rand_num = random.uniform(0, 1)
        for word, freq in freq_word.items():
            prob = freq / freq_den[h]
            sum_prob += prob
            if rand_num < sum_prob:
                if word != "<end>": 
                    sentence += word + " "
                ngram_arr.append(word)
                if len(ngram_arr) > n - 1:
                    ngram_arr.pop(0) 
                break

    return sentence.capitalize().rstrip()

# Function to Create Sentences for n-grams. 
def create_sen(m, num, den, n):
    for o in range(0, m):
        sen = sentence(num, den, n)
        print(str(o+1) +":" + sen)
    
def main():
    # Checks if the the correct command line arguments are provided. 
    if len(sys.argv) <4:
        print("Please enter ngram.py n m input_file1.txt inputfile2.txt ...")
        return
    # Stores the values from command lines into variables. 
    n = int(sys.argv[1])
    num_sentence = int(sys.argv[2])
    
    # Checks if N and M are valid. 
    if n < 1:
        print("n can not be less than 1")
        exit()
    if num_sentence < 1:
        print("m cannot be less than 1")
        
    # Read the Text from the input files. 
    text = ""
    for text_file in sys.argv[3:]:
        with open(text_file, "r", encoding="utf-8") as file:
            text +=file.read()
         
    # if 1-gram. 
    if n == 1:
        ngrams = create_ngram(text, n)
        freq_word = {}
        for w in ngrams:
            if w in freq_word:
                freq_word[w] += 1
                continue
            freq_word[w] = 1
        sum_words = sum(freq_word.values()) - freq_word["<end>"]
        
        for num_sentence in range (0, num_sentence):
            sen = uni(sum_words, freq_word)
            print(str(num_sentence+1) + ": " + sen)
    # If more than 1
    elif n > 1:
        ngrams = create_ngram(text, n)
        num = numerator(ngrams, n)
        den = denominator(ngrams, n)
        create_sen(num_sentence, num, den, n)

if __name__ =="__main__":
    main()

            
            
            
            
            