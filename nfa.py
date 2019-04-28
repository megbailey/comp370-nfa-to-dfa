class NFA:
    def __init__(self):
        self.num_states = 0
        self.states = []
        self.alphabet = []
        self.num_transitions = 0
        self.transition_functions = []
        self.accept_states = []

    def initNFA(self, input_string):

        input_iter = iter(input_string)

        self.num_states = next(input_iter)
        alphabet_str = next(input_iter)
        for char in alphabet_str:
            self.alphabet.append(char)

        transition = next(input_iter)
        while "\'" in transition:
            transition = transition.replace("\'", "")

            #adding to our list of states
            transition_ar = transition.split()
            first_state = transition_ar[0]
            second_state = transition_ar[2]
            if first_state not in self.states:
                self.states.append(first_state)
            if second_state not in self.states:
                self.states.append(second_state)

            self.transition_functions.append(transition_ar)
            transition = next(input_iter)
            self.num_transitions += 1

        self.start_state = next(input_iter)
        accept_states_string = next(input_iter).strip()
        self.accept_states = accept_states_string.strip().split(" ")


    def _printSelf(self):
        print("Num States: " + str(self.num_states))
        print("Alphabet: " + str(self.alphabet))
        print("Start State: " + str(self.start_state))
        print("Accept States: " + str(self.accept_states))
        print("Num Transitions: " + str(self.num_transitions))
        print("States: " + str(self.states))
        print("Transition Functions: " + str(self.transition_functions))