#-------------------------------------------------------
#Sajesh Sahoo
#1/28/2024
#NLP 416
#This is a python program that creates a Therapist called Eliza, That will listen to your problems, and help you. 
#To start the program the input should be just your name for ex. (Sajesh), and then the input for this program would be anything you feel for ex: I am sad, I am hungry, I am depressed.
#And the output will result in Eliza asking questions based on your input.
#and to end the conversation type quit, exit, bye, or goodbye.
#To use the program, open the CDM (Command Prompt), locate where the program is located, and use cd ___, for ex. cd Desktop, or cd Downloads. And then use the command, python eliza.py.
#I used a algorithm that searches for a word that the user inputted, and if the word matches the one of the words listed in the responses then eliza prints out the specific response.
#and if the input has no match then eliza asks "I'm not sure I understand. Can you tell me more?".
#-------------------------------------------------------
import re

class eliza:
    def __init__(self):
        #Contains the regular expressions as keys and the coressponding responses.
        self.responses = {
            r'\bhello\b|\bhi\b': ["Hi! I'm a psychotherapist. What is your name?"],
            r'\bmy name is (.*)\b': ["Hi {0}. How can I help you today?"],
            r'\bfailed (.*)\b': ["Why do you think you failed?"],
            r'\bfail (.*)\b': ["Why do you think you will fail?"],
            r'\bfailure (.*)\b': ["Why do you think you are a failure"],
            r'\bis it (.*)\b': ["If it was, How would you feel?"],
            r'\bi want (.*)\b': ["Why do you want {0}?"],
            r'\bi feel (.*)\b': ["When you feel {0}, what do you do?"],
            r'\bi dont think (.*)\b': ["Why do you think that?"],
            r'\bwhat (.*)\b': ["Why do you ask?"],
            r'\bhow (.*)\b': ["How do you think?"],
            r'\bi am (.*)\b': ["Why are you {0}? "],
            r'\bi would (.*)\b': ["Could you explain why you would do that?"],
            r'\b(crave|craving)\b': ["Why don't you tell me more about your cravings?"],
            r'\bis there (.*)\b': ["do you think there is {0}"],
            r'\b(eat|eaten|ate)\b': ["What do you want to eat?"],
            r'\bthrew (.*)\b': ["Why did you throw {0}?"],
            r'\bthrow (.*)\b': ["Why thow the {0}? [?]"],
            r'\byou\b': ["We are talking about you not me"],
            r'\bi was (.*)\b': ["Why were you {0}? "],
            r'\bfamily (.*)\b': ["Tell me more about your family"],
            r'\b(father|dad)\b': ["Tell me more about your father."],
            r'\b(mother|mom)\b': ["Tell me more about your mother."],
            r'\b(brother|sibling|sister)\b': ["Tell me more about your sibling."],
            r'\b(friend|friends)\b': ["Tell me more about your friends."],
            r'\bcan i (.*)\b': ["Do you think you can {0}"],
            r'\bsorry (.*)\b': ["No need to apologize."],
            r'\bit is (.*)\b': ["Are you sure it is {0}"],
            r'\b(work|working|worked) (.*)\b': ["How was work?"],
            r'\byes (.*)\b': ["Ok, can you elaborate a bit more?"],
            r'\b(quit|exit|bye|goodbye)\b': ["Thank You for talking with me!"],
            r'\b(thank You|Thanks)\b':["I am just doing my job, What else can I do for you?"],
            r'\b(sad|sadness)\b': ["Why are you sad?"],
            
        }
        
    #Methods to return outputs by matching the patterns in the response dictionary. 
    def respond(self, user_input):
        #for loop to loop through each pattern. 
        for pattern, responses in self.responses.items():
            #searches for match between the input and the current pattern. Converted to lowercase, to not have any issues. 
            match = re.search(pattern, user_input.lower())
            if match:
                #if the match is found then retuns the response
                response = responses[0]
                #if the response contains 0 then it replaces it with the user input
                if '{0}' in response:
                    response = response.format(*match.groups())
                return response
        #if no match is found then this is returned
        return "I'm not sure I understand. Can you tell me more?"
    
    def run(self):
        #starting the conversation
        print("-> [Eliza] Hi, I'm a psychotherapist. What is your name?")
        #user input name
        username = input("=> [user] ")
        print(f"-> [Eliza] Hi {username}. How can I help you today?")
        #interact with the user until the user decides to stop. 
        while True:
            userinput = input("=> [{}]: ".format(username))
            response = self.respond(userinput)
            print(f"-> [Eliza] {response}")
            if response == "Thank You for talking with me!":
                break

if __name__ == "__main__":
    eliza = eliza()
    eliza.run()
