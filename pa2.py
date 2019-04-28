import pprint
from nfa import NFA
from dfa import DFA

def main():
    input_string = readFile("testcasesUnix/nfa6.txt")
    
    nfa = NFA()
    nfa.initNFA(input_string)

    dfa = DFA()
    dfa.convertFromNfa(nfa)
    text_file = dfa.makeTextFile()
    
    dfa_input = readFile("testcasesUnix/dfa6Input.txt")
    dfa.simulateDFA(text_file, dfa_input)

def readFile(filename):
    file = open(filename, 'r')
    text_file = ''
    num_lines = 0
    #Placing text file in array so we can easily work with it and close the file
    for line in file:
        text_file += line
        num_lines += 1
    file.close()
    file_text = text_file.split('\n')
    text_file = []
    for line in file_text:
        text_file.append(line.replace('\n', ''))
    return text_file


    
main()
