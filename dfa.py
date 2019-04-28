import pprint

class DFA:

    def __init__(self):
        self.num_states = 0
        self.num_transitions = 0
        self.start_state = ""
        self.renamed_start_state = ""

        self.org_states = []
        self.renamed_states = []
        self.alphabet = []
        self.renamed_accept_states = []
        self.accept_states = []

        self.nfa_transition_dict = {}
        self.dfa_transition_dict = {}
        self.rename_dict = {}
        self.renamed_dfa_transition_dict = {}


    def convertFromNfa(self, nfa):
        self.num_states = int(nfa.num_states)
        self.alphabet = nfa.alphabet
        self.start_state = nfa.start_state
        
        #starting NFA and DFA dicitionaries
        for transition in nfa.transition_functions:
            starting_state = transition[0]
            transition_symbol = transition[1]
            ending_state = transition[2]
            
            key = (starting_state , transition_symbol)
            self.addToDFADictionary(key, ending_state)
            self.addToNFADictionary(key, ending_state)

            self.addtoStateList(starting_state)
            self.addtoStateList(ending_state)
     
        pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(self.dfa_transition_dict)
        self.makeSingleStatesAList()
        self.createEmptyTransitions() 
        #pp = pprint.PrettyPrinter(indent=4)
        self.epsilonEnclosure()
        #pp.pprint(self.dfa_transition_dict)
        #print(self.org_states)

        for key, value in self.dfa_transition_dict.items():   
            if len(value) > 1: #is multi-state
                self.getMultiStates(value)

        #pp.pprint(self.dfa_transition_dict)
        #print(self.org_states)
        self.makeDeadTransitions()
        #pp.pprint(self.dfa_transition_dict)
        self.rename()
        self.getAcceptStates(nfa)
        self.num_transitions = len(self.renamed_dfa_transition_dict.keys())

    def addtoStateList(self, state):
        if not isinstance(state, list):
            state = [state]
        state = sorted(state)
        if state not in self.org_states and len(state) is not 0: #not empty
            self.org_states.append(state)
   
    def addToDFADictionary(self, key, value):
        if key in self.dfa_transition_dict:
            for state in value:
                self.dfa_transition_dict[key].append(state)
        else:
            if isinstance(value, list):
                self.dfa_transition_dict[key] = value
            else:
                self.dfa_transition_dict[key] = [value]
        self.sortQB(key)
    
    def addToNFADictionary(self, key, value):
        if key in self.nfa_transition_dict:
            self.nfa_transition_dict[key].append(value)
        else:
            self.nfa_transition_dict[key] = [value]

    def getMultiStates(self, value):
        for symbol in self.alphabet:
            #recursion case
            if (str(value), symbol) not in self.dfa_transition_dict and len(value) is not 0: #not empty []
                multi_state_ending_ar = []
                multi_state_ending = []
                for org_state in value:
                    if (str([org_state]), symbol) in self.dfa_transition_dict:
                        multi_state_ending_ar.append(self.dfa_transition_dict[(str([org_state]) , symbol)])
                        multi_state_ending_ar = sorted(multi_state_ending_ar)
                        for multi_state in multi_state_ending_ar:
                            for state in multi_state:
                                if state not in multi_state_ending:
                                    multi_state_ending.append(state)
                                    multi_state_ending = sorted(multi_state_ending)

                key = (str(value), symbol)
                self.addToDFADictionary(key, multi_state_ending)
                self.addtoStateList(multi_state_ending)

                self.getMultiStates(multi_state_ending)
                
            #base case - dont do anything
            else:
                break


    def createEmptyTransitions(self):
        #creating empty transitions for our inital states
        for state in self.org_states:
            for symbol in self.alphabet:
                if (str(state), symbol) not in self.dfa_transition_dict:
                    self.dfa_transition_dict[(str(state), symbol)] = []


    def makeSingleStatesAList(self):
        #clean up keys that only have single element and make sure they are always a list
        for key, value in self.dfa_transition_dict.items(): 
                if '\'' not in key[0]: #its not a list
                    for symbol in self.alphabet:
                        if (key[0], symbol) in self.dfa_transition_dict:
                            self.dfa_transition_dict[ ( str( [key[0]] ) , symbol ) ] = self.dfa_transition_dict[(key[0] , symbol )]
                            del self.dfa_transition_dict[(key[0], symbol)]

    def makeDeadTransitions(self):
        #making a dead state
        dead_state = str(self.num_states + 1)
        self.num_states += 1
        for state in self.org_states:
            for symbol in self.alphabet:
                if (str(state), symbol) not in self.dfa_transition_dict or len(self.dfa_transition_dict[(str(state), symbol)]) is 0:
                    self.dfa_transition_dict[(str(state), symbol)] = [dead_state]
            
        #adding the dead state to our list of states and transition functions
        self.org_states.append([dead_state])
        for symbol in self.alphabet:
            self.dfa_transition_dict[(str([dead_state]), symbol)] = [dead_state]



    def epsilonEnclosure(self):
        for e_key, e_value in self.dfa_transition_dict.items():
            
            e_starting_state = e_key[0]
            e_symbol = e_key[1]
            e_ending_state = e_value
            all_e_enclosure = []
            queue = []

            if e_symbol is 'e': #we have an epsilon state
                #print(e_key) 
                #starting our stack
                for state in e_ending_state:
                    queue.append(state)
                    all_e_enclosure.append(state)
                #print(e_ending_state)
                while len(queue) is not 0:
                    e_state = queue.pop()
                    if (e_state, 'e') in self.dfa_transition_dict: #and e_state not in all_e_enclosure:
                        for state in self.dfa_transition_dict[(e_state, 'e')]:
                            all_e_enclosure.append(state)
                            queue.append(state)

                for symbol in self.alphabet:
                    e_final = []
                    for state in all_e_enclosure:
                        if (str([state]), symbol) in self.dfa_transition_dict:
                            for qb in self.dfa_transition_dict[(str([state]), symbol)]:
                                if qb not in e_final:
                                    e_final.append(qb)
                    #print(str([e_starting_state])+ " " + symbol + " " + str(e_final))
                    key = (str([e_starting_state]) , symbol)
                    self.addToDFADictionary(key, e_final)
                    self.addtoStateList(self.dfa_transition_dict[key])

                self.addtoStateList(e_final)
                self.addtoStateList(all_e_enclosure)
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(self.dfa_transition_dict)

        #now we've taken care of all the epsilon junk - delete the epsilon transition from dict
        for e_key, e_value in self.dfa_transition_dict.items():
            e_symbol = e_key[1]
            if e_symbol is 'e': #we have an epsilon state       
                del self.dfa_transition_dict[e_key]




    def getAcceptStates(self, nfa):
        for key, value in self.dfa_transition_dict.items():
            for accept_state in nfa.accept_states:
                if accept_state in value and value not in self.accept_states:
                    self.accept_states.append(value)
        for accept_state in self.accept_states:
            self.renamed_accept_states.append(self.rename_dict[str(accept_state)])




    #renaming inital multi-states
    def rename(self):
        rename_counter = 1
        for key, value in self.dfa_transition_dict.items():
            if key[0] not in self.rename_dict.keys():
                self.rename_dict[key[0]] = rename_counter
                rename_counter += 1
            if str(value) not in self.rename_dict.keys():
                self.rename_dict[str(value)] = rename_counter
                rename_counter += 1
        for key, value in self.dfa_transition_dict.items():
            state = key[0]
            symbol = key[1]
            if state in self.rename_dict.keys() and str(value) in self.rename_dict.keys():
                self.renamed_dfa_transition_dict[(self.rename_dict[state], symbol)] = self.rename_dict[str(value)]
            else:
                print("ERROR: RENAME DICT IS WRONG")
        for key, value in self.rename_dict.items():
            self.renamed_states.append(value)
        all_states = self.renamed_states
        sorted_states = sorted(all_states)
        self.renamed_states = sorted_states
        self.renamed_start_state = self.rename_dict[str([self.start_state])]
 
    def sortQB(self, key):
        qb = self.dfa_transition_dict[key]
        qb = sorted(qb)
        self.dfa_transition_dict[key] = qb

    def printRenamedDict(self):
        for key, value in self.rename_dict.items():
            print(str(key) + " => " + str(value))

    def printDFA(self):
        pp = pprint.PrettyPrinter(indent=4)
        print("Num States: " + str(self.num_states))
        print("Alphabet: " + str(self.alphabet))
        print("Start State: " + str(self.start_state))
        print("Accept States: " + str(self.accept_states))
        print("States: " + str(self.org_states))
        print("Transition Functions: ")
        pp.pprint(self.dfa_transition_dict)

    def printRenamedDFA(self):
        pp = pprint.PrettyPrinter(indent=4)
        print("Num States: " + str(self.num_states))
        print("Alphabet: " + str(self.alphabet))
        print("Renamed Start State: " + str(self.renamed_start_state))
        print("Renamed Accept States: " + str(self.renamed_accept_states))
        print("Renamed States: " + str(self.renamed_states))
        print("Renamed Transition Functions: ")
        pp.pprint(self.renamed_dfa_transition_dict)

    def makeTextFile(self):
        text_file = ""
        alphabet = ""
        text_file += str(len(self.renamed_states)) + '\n'
        for symbol in self.alphabet:
            alphabet += symbol
        text_file += alphabet + '\n'
        for key, value in self.renamed_dfa_transition_dict.items():
            transition = str(key[0]) + " '" + str(key[1]) + "' " + str(value) + '\n'
            text_file += transition      
        text_file += str(self.renamed_start_state) + '\n'
        accept_states = ""
        for state in self.renamed_accept_states:
            accept_states = (accept_states + " " + str(state)).strip()
        text_file += accept_states + '\n'
        return text_file

    def simulateDFA(self, text_file, dfa_input):
        dictionary = {}
        num_lines = 0

        num_lines += 1
        text_file = text_file.split('\n')
        num_states = text_file[0]
        alphabet = text_file[1]
        count = 2
        
        for transition in text_file:
            #print(transition)
            if "\'" in transition:
                transition_ar = transition.replace('\'', '').split()    
                transition = transition_ar[0] + '-' + transition_ar[1]
                dictionary[transition] = transition_ar[2]
                count += 1
        start_state = text_file[count]
        accept_states_ar = text_file[count+1].split()
        count += 2
        line_count = 0
        for line in dfa_input:
            line_count += 1
        count = 0
        for line in dfa_input:
            if count is not line_count-1: #not the last line. we know this will be empty
                #state = start_state
                qa = start_state
                for c in line:
                    if c in alphabet:
                        #transition = state + '-' + c
                        transition = qa + '-' + c
                        #state = dictionary[transition]
                        qb = dictionary[transition]

                        for key, value in self.rename_dict.items():
                            #print(str(value) + " " + str(state))
                            if str(value) is str(qb):
                                qb_translated = key
                            if str(value) is str(qa):
                                qa_translated = key

                        #print(str(qa_translated) + "(" + str(qa) + ") \'" + c + "\'  => " + str(qb_translated) + "(" + str(qb) + ")")
                        #print("Dictionary: " + str(qa_translated) + " '" + c + "' => " + str(self.dfa_transition_dict[(qb_translated, c)]))
                        #print(transition + " => " + str(qb))
                        qa = qb
                count += 1
                if qa in accept_states_ar:
                    print("Accept")
                else:
                    print("Reject")  




