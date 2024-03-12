"""
PA-3 Word Sense Disambiguation.
Sajesh Sahoo
3-11-2024
CMSC-416

#The main purpose of this program is given the corpus, this program uses it as a training data to teach a model
the learned model is then used by the program on a test corpus to identify wether it matches with the sense phone or product.

#To use the program have all the files in the same directory. line-test.txt, line-train.txt, line-key.txt, you do not need to worry
about my-model.txt, adn my-line-answers.txt, as the program will produce them.
then open the command prompt and use Cd .. to locate the directory all ur files are located at, Ex. cd desktop.
you can either use python or python3 if u have it installed:
you can use python wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt
or python3 wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt

To check the output of this program, open the file location, and check the my-line-answers.txt, adn the model to see the instances.
the output should look something similar to:
<answer instance="line-n.w8_059:8174:" senseid="phone"/>
<answer instance="line-n.w7_098:12684:" senseid="phone"/>
<answer instance="line-n.w8_106:13309:" senseid="phone"/>
<answer instance="line-n.w9_40:10187:" senseid="phone"/>
<answer instance="line-n.w9_16:217:" senseid="phone"/>
<answer instance="line-n.w8_119:16927:" senseid="phone"/>
<answer instance="line-n.w8_008:13756:" senseid="phone"/>
<answer instance="line-n.w8_041:15186:" senseid="phone"/>
<answer instance="line-n.art7} aphb 05601797:" senseid="phone"/>
<answer instance="line-n.w8_119:2964:" senseid="phone"/>
<answer instance="line-n.w7_040:13652:" senseid="phone"/>
<answer instance="line-n.w7_122:2194:" senseid="phone"/>
<answer instance="line-n.art7} aphb 45903907:" senseid="phone"/>
<answer instance="line-n.art7} aphb 43602625:" senseid="phone"/>
<answer instance="line-n.w8_034:3995:" senseid="phone"/>
<answer instance="line-n.w8_139:696:" senseid="phone"/>
<answer instance="line-n.art7} aphb 20801955:" senseid="phone"/>
...

The algorithm of the code:
The code takes in the training file, cleans the data, finds all the matches for the different senses, and then the senses are
extracted from the matches and stored in the model file, then the test files are taken in then preprocessed, and then finds
the matches of the senses, then the it puts the matches list in to a text, as well as finds the instances and then it the
program uses the matches list, phone sense and profuct sense from the training data, stored in the model file to predict
the test file, and outputs it into the my-line-answers.txt.

Report From scorer.py:
Accuracy = 57.937 %
Baseline Accuraxy = 57.143 %
Actual     phone  product  All
Predicted
phone         72        0   72
product       54        1   55
All          126        1  127

"""
import re
from sys import argv

#Preprocess Text
def preprocessed(text):
    #Remove tags and punctuations from texts. 
    text = re.sub(r'<@>|(<|<\/)[pshead]+>', "", text)
    return text
#Extarct keywords
def extract_senses(matches, keyword):
    #Return the match containing the keyword
    return [match for match in matches if keyword in match]
#count the occurence of sense in the list
def count_senses(sense_list, keyword_list):
    return sum(1 for sense in sense_list if sense in keyword_list)

#Predict the sense
def predict_sense(matches, phone_sense, product_sense):
    #store predictions
    sense_predictions = []
    #iterate through all the matches
    for match in matches:
        phone_count = count_senses(match, phone_sense)
        product_count = count_senses(match, product_sense)
        #determine the sense based on its count
        if phone_count > product_count:
            sense_predictions.append("phone")
        elif phone_count < product_count:
            sense_predictions.append("product")
        else:
            sense_predictions.append("phone")#default
    return sense_predictions

if __name__ == "__main__":
    #get the files from the command line argument
    train_file = argv[1]
    test_file = argv[2]
    model_file = argv[3]

    #read and preprocess the training data. 
    with open(train_file, "r") as tr:
        train_text = tr.read()
    train_text = preprocessed(train_text)
    #find all the matches in the training data. 
    train_matches = re.findall(r'<\s*answer.*?senseid\s*=\s*"(.*?)".*?>\s*<\s*context\s*>\s*(.*?)\s*<\s*\/context\s*>\s*<\s*\/\s*instance\s*>', train_text)

    phone_sense_matches = extract_senses(train_matches, "phone")#extract phone sense
    product_sense_matches = extract_senses(train_matches, "product")#extract product sense

    #read and preprocess the text data. 
    with open(test_file, "r") as ts:
        test_text = ts.read()
    test_text = preprocessed(test_text)
    test_matches = re.findall(r'<\s*instance\s*(.*)>\s*<\s*context\s*>\s*(.*?)\s*<\s*\/context\s*>\s*<\s*\/\s*instance\s*>', test_text) #find the matches in the test data
    matches_text = [' '.join(lists) for lists in test_matches]#join the matches list into a string
    ids = re.findall(r'<\s*instance.(.*)\s*>', test_text)#find all the intances of <instance id=line-n.w...:">
    answers = [x[4:-1] for x in ids]# extracts position 4 to the last position for each index in ids. 

    #prediction for the test data
    sense_predictions = predict_sense(matches_text, phone_sense_matches, product_sense_matches)
    #output for each instance
    for answer, sense in zip(answers, sense_predictions):
        print(f"<answer instance=\"{answer}\" senseid=\"{sense}\"/>")
