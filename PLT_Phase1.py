import re

Last_ID = 0

class state:
    def __init__(self):
        global Last_ID
        self.ID = Last_ID
        Last_ID += 1
        self.next_states = []
        self.token = None
        self.is_start = 0
        self.is_final = 0
        self.final_reachable_state = None

    def print_state(self):
        # print(self.ID, self.next_states, self.next_states[1][1].next_states, self.next_states[0][1].next_states[0][1].next_states[0][1].next_states, 
        #         self.next_states[0][1].next_states[0][1].next_states[0][1].token)
        print(self.ID, self.next_states)    


def add_next_state(current_state, input_char):
    next_state = state()
    current_state.next_states.append((input_char, next_state))
    current_state.final_reachable_state = next_state


def join_two_states(current_state, next_state, input_char):
    current_state.next_states.append((input_char, next_state))


def priority(regex_operator):
    
    if regex_operator == '|':
        return 0
    elif regex_operator == '-':
        return 1
    elif regex_operator == '.':
        return 2
    elif regex_operator == '+' or regex_operator == '*':
        return 3
    elif regex_operator == '(':
       return  4

def infix_to_postfix(regex_infix):
    regex_postfix = ""
    stack = []
    regex_operators = {'(', '|', '-', '.', '+', '*'}
    i = 0
    while i < len(regex_infix):
        
        if regex_infix[i].isalpha():
            while(i < len(regex_infix)  and regex_infix[i].isalpha()): 
                regex_postfix += regex_infix[i]
                i += 1
            regex_postfix += " "
        
        elif regex_infix[i] in regex_operators:
            # print(stack, regex_infix[i])
            while(len(stack) != 0 and priority(stack[-1]) >= priority(regex_infix[i]) and stack[-1] != '('):
                regex_postfix = regex_postfix + stack.pop() + " "
            stack.append(regex_infix[i])
            i += 1
        
        elif regex_infix[i] == ')':
            # print(stack)
            while(stack[-1] != '('):
                regex_postfix = regex_postfix + stack.pop() + " "
            stack.pop()
            i += 1

        elif regex_infix[i] == "\\":
            regex_postfix = regex_postfix + '\\' + regex_infix[i+1] + " "
            i += 2
        
        else:
            regex_postfix = regex_postfix + regex_infix[i] + " "
            i += 1

    while(len(stack) != 0):
        regex_postfix = regex_postfix + stack.pop() + " "
    return regex_postfix
    

def or_states(states):
    new_end_state = state()
    new_start_state = state()
    new_start_state.final_reachable_state = new_end_state
    for s in states:
        join_two_states(new_start_state, s, 'eps')
        join_two_states(s.final_reachable_state, new_end_state, 'eps')
    return new_start_state  


def concat_states(state1, state2):
    join_two_states(state1.final_reachable_state, state2, 'eps')
    state1.final_reachable_state = state2.final_reachable_state
    return state1


def repeat(current_state, is_one_or_more):
    new_end_state = state()
    new_start_state = state()
    new_start_state.final_reachable_state = new_end_state
    join_two_states(new_start_state, current_state, 'eps')
    join_two_states(current_state.final_reachable_state, new_end_state, 'eps')
    join_two_states(current_state.final_reachable_state, current_state, 'eps')
    if not is_one_or_more:
        join_two_states(new_start_state, new_end_state, 'eps')
    return new_start_state


def evaluate_postfix(regex_postfix, token):
    stack = []
    states = []
    i = 0
    while i < len(regex_postfix):

        if regex_postfix[i] == " ":
            i += 1

        elif regex_postfix[i] == '|':
            # print(stack)
            state1 = stack.pop()
            state2 = stack.pop()
            result = or_states([state1, state2])
            # print('res', result)
            stack.append(result)  
            i += 1

        elif regex_postfix[i] == '.':
            state1 = stack.pop()
            state2 = stack.pop()
            result = concat_states(state2, state1)
            stack.append(result)  
            i += 1

        elif regex_postfix[i] == '-':
            state1 = stack.pop()
            state2 = stack.pop()
            char1 = state2.next_states[0][0]
            char2 = state1.next_states[0][0]
            start_ascii = ord(char1) + 1
            end_ascii = ord(char2)
            states.append(state1)
            while start_ascii < end_ascii:
                input_char = chr(start_ascii)
                new_state = state()
                add_next_state(new_state, input_char)
                states.append(new_state)
                start_ascii += 1
            states.append(state2)
            # print(len(states))
            result = or_states(states)
            states.clear()
            stack.append(result)  
            i += 1

        elif regex_postfix[i] == '+':
            state1 = stack.pop()
            result = repeat(state1, 1)
            stack.append(result)  
            i += 1

        elif regex_postfix[i] == '*':
            state1 = stack.pop()
            result = repeat(state1, 0)
            stack.append(result)  
            i += 1

        elif regex_postfix[i] == '\\':
            input_char = regex_postfix[i+1]
            new_state = state()
            if input_char == 'L':
                add_next_state(new_state, 'eps')
            else:
                add_next_state(new_state, input_char)
            stack.append(new_state)
            i += 2

        else:
            # print(regex_postfix[i])
            input_char = regex_postfix[i]
            new_state = state()
            add_next_state(new_state, input_char)
            stack.append(new_state)
            i += 1 

    result = stack.pop()
    result.final_reachable_state.is_final = 1
    result.final_reachable_state.token = token
    return result


def nfa_join(to_nfa_join):
    new_start_state = state()
    for nfa_s in to_nfa_join:
        join_two_states(new_start_state, nfa_s, 'eps')
    return new_start_state



def read_lexical_file():
    lexical_file = open("dummylex.txt", "r")
    lexical = lexical_file.read()
    lexical = lexical.split('\n')

    regular_definitions = {}
    token_priorities = []
    to_nfa_join = []
    subs_token = ""
    for lex in lexical:    
        if len(lex) > 0 and lex[0] != '{' and lex[0] != '[' and lex[0] != '(':
            lex = re.sub('[" \t"]', '', lex)
            for c in lex:
                if c == '=':
                    symbol = "="
                    break
            
                elif c == ':':
                    symbol = ':'
                    break

            lex = re.split('[=:]', lex, maxsplit=1)
            token = lex[0]
            regex = lex[1]
            subs_regex = regex
            i = 0
            while i < len(regex):
                if regex[i].isalpha():
                    while(i < len(regex)  and regex[i].isalpha()): 
                        subs_token += regex[i]
                        i += 1
                    if len(subs_token) > 1:
                        if subs_token in regular_definitions:
                            # print(subs_regex, subs_token, regular_definitions[subs_token])
                            subs_regex = subs_regex.replace(subs_token, '('+regular_definitions[subs_token]+')', 1)
                            # print(subs_regex)
                        else:
                            print("regular definition doesn't exist")
                            exit() 
                    subs_token = ""                                     
                else:
                    i += 1
                
            regular_definitions[token] = subs_regex             
            # print(regular_definitions)
            if symbol == ':':          
                regex_postfix = infix_to_postfix(subs_regex)
                # print(regex_postfix)
                result = evaluate_postfix(regex_postfix, token)
                to_nfa_join.append(result)
                token_priorities.append(token)

        else:
            # to_or = []
            words = lex[1:-1].split()
            for w in words:
                token_priorities.append(w)
                if len(w) > 1:
                    state1 = state()
                    add_next_state(state1, w[0])
                    state2 = state()
                    add_next_state(state2, w[1])
                    j = 1
                    while True:
                        result = concat_states(state1, state2)
                        if j == len(w) - 1:
                            break
                        state1 = result
                        state2 = state()
                        add_next_state(state2, w[j+1])
                        j += 1
                else:
                    result = state()
                    add_next_state(result, w)

                if lex[0] == '{' or lex[0] == '[':
                    result.final_reachable_state.is_final = 1
                    result.final_reachable_state.token = w
                    # to_or.append(result)
                    to_nfa_join.append(result)
                    # print("innnnnnnnnnnnn")
                    # print('+++++++++++tok', result.final_reachable_state.token)
                else:
                    result = repeat(result, 1)
                    # to_or.append(result)
                    to_nfa_join.append(result)

            # result = or_states(to_or)

            # to_nfa_join.append(result)
            # to_or.clear()
    # for t in to_nfa_join:
        # print('toooookeeeeeeeeen',t.final_reachable_state.token)
    start_state = nfa_join(to_nfa_join)
    return start_state, token_priorities
                
    


# read_lexical_file()

# res = evaluate_postfix('\+ \- | ', "letter")
# res.print_state()
# print(Last_ID)

###########################################################################################################


from collections import defaultdict

global dfa_nodes #, epsilon, token_priority_list

Last_ID =0  
epsilon = "eps"      # set this one to epsilon symbol 
token_priority_list = [] # set this one to ordered token prority list

trans = []               # u don't have to mess with this one if u must however set it to a list of 
                         # all possible transition characters 
dfa_nodes = []           # Don't mess with this one

# class state:
#     def __init__(self,token,is_final):
#         global Last_ID
#         self.ID =Last_ID
#         Last_ID +=1
#         self.token = token
#         self.next_states = []
#         self.is_final = is_final

class dfa_node:
    def __init__(self,is_start,is_final):
        self.is_start = is_start
        self.is_final = is_final
        self.next = defaultdict(lambda x = self:x)
        self.ndfaset = []
        self.token = None

    def expand_d_node(self):
        for i in self.ndfaset :
            for j in i.next_states:
                if j[0] == epsilon:
                    if j[1] not in self.ndfaset:
                        self.ndfaset.append(j[1])
                        self.expand_d_node()

    def finish(self):
        for i in self.ndfaset:
            if i.is_final:
                self.is_final = True
                return True
        self.is_final = False
        return False

    def insert_token(self):
        # if self.is_final:
        for t in token_priority_list:
            for i in self.ndfaset:
                if t == i.token:
                    #print(':::::::::::::::::::::::', i.token)
                    self.token = t
                    return
                
dead_node = dfa_node(False,False)
   
def check_if_exist(d_node:dfa_node):
    for i in dfa_nodes:
        if d_node.ndfaset == i.ndfaset:
            return i
    return False


def to_dfa(d_node:dfa_node):
    for i in trans:
        dead_char = True
        new_node = dfa_node(False , False)
        for k in d_node.ndfaset:
            for j in k.next_states:
                if j[0] == i:
                    dead_char = False
                    new_node.ndfaset.append(j[1])
     
        if dead_char :
            d_node.next.update({ i : dead_node })
        else :
            new_node.expand_d_node()
            new_node.ndfaset.sort(key = lambda x : x.ID , reverse = False)
            s = check_if_exist(new_node)
            if s:
                d_node.next.update({ i : s })
                #return
            else :
                if new_node.finish():
                    new_node.insert_token()
                d_node.next.update({ i : new_node })
                dfa_nodes.append(new_node)
                to_dfa(new_node)
                
trans_nodes = []                
def get_all_trans(node:state):
    #if node.is_final:
    #    #print('32141343523',node.token)
    if node in trans_nodes:
        return
    trans_nodes.append(node)
    for i in node.next_states:
        if i[0] not in trans and i[0] != epsilon:
            trans.append(i[0])
        get_all_trans(i[1])


def to_dfa_init(node:state):
    get_all_trans(node)
    d_node = dfa_node(True , node.is_final)
    d_node.ndfaset.append(node)
    d_node.expand_d_node()
    d_node.ndfaset.sort(key = lambda x : x.ID , reverse = False)
    if d_node.finish():
        d_node.insert_token()
    dfa_nodes.append(d_node)
    to_dfa(d_node)
    return d_node



def equate(node1 : dfa_node , node2 : dfa_node):
    for node in dfa_nodes:
        for i in node.next.keys():
            if node.next[i] == node2:
                node.next[i] = node1

def minimize_set(set , is_non_final_set):
    for i in range(len(set)):
        for j in range(i+1,len(set)):
            if set[i].next == set[j].next:
                if set[i].token == set[j].token or is_non_final_set:
                    #equate the two , as in all references to j are modified to reference i then del j
                    equate(set[i],set[j])
                    del set[j]
                    return True
    return False

def minimize_dfa():
    global dfa_nodes
    terminal_nodes = []
    non_terminal_nodes = []
    for d_node in dfa_nodes:
        if d_node.is_final:
            terminal_nodes.append(d_node)
        else :
            non_terminal_nodes.append(d_node)
    dont_stop = True
    while(dont_stop):
        dont_stop = minimize_set(terminal_nodes , False) | minimize_set(non_terminal_nodes , True)
    dfa_nodes = terminal_nodes + non_terminal_nodes
           

start_state, token_priority_list = read_lexical_file()
#print('########', token_priority_list)
dfa_s = to_dfa_init(start_state)
# to_dfa_init(res)
minimize_dfa()
#for node in dfa_nodes:
    # print(node, node.next, node.is_start, node.is_final, node.token)
    #print('innnnnnnnnnnnnnnnnnnnnnn', node.token)

# #############################################################################################################



def panic_mode_recovery():
    pass


delimters = [" ",",",  ";", "(", ")", "\n"]
operations = ["+", "-", "*", "/", "=",":"]
try:
    f = open("case1.txt", "r")
except:
    print("file not found")

# print(f.read())
output = ""
word = ""
string = ""  
token = ""
dfa = dfa_s
dfa2 = dfa_s
# line
# print(dfa)

z = 0
test = [] 


"""    
for x in f:
    # print(x)
    word = ""
   
    for o in range(len(x)):
        if ((x[o] in delimters) or  (x[o] in operations)):
            
            print("x:word",x[o],word)
            
            
            dfa = dfa_s
           
            for i in word:
                dfa = dfa.next[i]
                
            if((x[o-1] != " ") or (x[o-1] != "\n")):
                if(dfa.is_final):
                    z = z + 1
                    output = output + "\n" + dfa.token #+ " " + i
                    test.append(dfa.token)
                    tok = dfa.token
                    if((test[len(test)-1]  == "relop" ) and (tok == "relop")):
                        pass
                        test.pop()
                        tok = ""  
                
            if(x[o] != " "):
                dfa = dfa_s
                dfa = dfa.next[x[o]]
                
                print("dfa x",x[o])
                if(dfa.is_final):
                    print("dfa token",dfa.token)
                    output = output + "\n" + dfa.token #+ " " + x[o] + "hh"
                    test.append(dfa.token)
                    tok = dfa.token
                     
                    dfa = dfa_s
            word = ""
            i= ""
            string = string + x[o]
            
        else:
            word = word + x[o]
            print("z",word,len(word),"z")
"""
"""
lis = []
token = ""
for x in f:
    # print(x)
    word = ""
    dfa= dfa_s
    for o in range(len(x)):
       
        if(x[o] != " "):
            dfa2 = dfa
            dfa = dfa.next[x[o]]
            if(dfa.is_final):
                token = dfa.token
                print(token)
            elif(dfa2.is_final):
                dfa = dfa_s
                token = dfa.token
                
            
        else:
            #dfa.next[x[o]]
            pass
            output = output + "\n"+ token
            
"""
def error_recovery(word):
    dfa = dfa_s
    for i in word:
        dfa = dfa.next(i)
    if(dfa.is_final):
        return dfa
    else:
        word = word[:-1]
        error_recovery(word)
dfa = dfa_s
word = ""
err = ""
for x in f:
    for o in range(len(x)):
        if((x[o] == " ") or (x[o] == "\n") or (x[o] == "\t")):
            if(dfa.is_final):
                token = dfa.token
            
                output = output + "\n"+ token
                dfa = dfa_s
                #
        if(dfa.next[x[o]] == dead_node):
            token = dfa.token
            output = output + "\n"+ token
            dfa = dfa_s
            #print("yes")
            dfa = dfa.next[x[o]]
            print("error handled in line\n\t",x)

              
            # else:
            #     print("error")#,x[o-2],x[o],x[o+1])
            #     dfa = dfa_s
            #     for j in range(o-1):
            #         dfa = dfa.next[x[j]]
                
            #     output = output + "\n"+ dfa.token
            #     dfa = dfa_s
            #     o=o-1
            #     #dfa = dfa.next[x[o-1]]
            #     #dfa = dfa.next[x[o]]
            #     #output = output + "\n"+ dfa.token
            #     #dfa = error_recovery(word)
            #     #output = output + "\n"+ dfa.token
            #     #dfa = dfa_s
            #     pass
            
        else:
            dfa = dfa.next[x[o]]
    if(dfa.is_final):
        token = dfa.token
        output = output + "\n"+ token

            
f.close()
# print(output)
# print(test)
#print("############output###########")

w = open("output.txt", "w")
w.write(output+'\n$')
w.close()


f = open('tokens.txt', 'w')
for token in token_priority_list:
    f.write(token+'\n')
f.write('$')
f.close()

# s = ""
# for i in test:
#     s = s + "\n" + i
# lol = open("output2.txt", "w")
# lol.write(s)
# lol.close()

# print("############test###########")
# z=" "
# if(z != " "):
#     print("yes")
# print(z)
# dfa = dfa_s

# dfa = dfa.next[':']
# dfa = dfa.next['=']


# if(dfa == dead_node):
#     print("ji")

# print(dead_node)
# print(dfa)
# print(dfa.token)
# #print(string)