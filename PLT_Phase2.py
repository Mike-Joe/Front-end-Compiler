import re
import copy
from collections import defaultdict
from bonus import read_file , find_if_common , mickeyfy




records = read_file("input_CFG_LL.txt")
find_if_common(records)
mickeyfy(records)
# for recor in records:
#     print(recor.mickey)


nonterminals = []
terminals = []
epsilon = '\L'
sync = 'sync'

def get_nonterminal(name):
    # print(name)
    # print("$$$$$$$$$")
    for nonterminal in nonterminals:
        # print(nonterminal.name)
        if nonterminal.name == name:
            # print(nonterminal.first_set)
            return nonterminal

def get_next_terminal(string):
    i = 1
    terminal = ''
    while True:
        if string[i] != '\'':
            terminal += string[i]
        else:
            break
        i += 1
    return terminal



class nonTerminal_symbol:
    def __init__(self, name):
        self.name = name
        self.is_start = 0
        self.is_first_calculated = 0
        self.production_set = []
        self.first_set = []   # [('c', 'cB'), ()]  'c': nonterminal token, 'cB': production
        self.follow_set = []

    def calculate_first_set(self):
        if self.is_first_calculated:
            return copy.deepcopy(self.first_set)
        else:
            for production in self.production_set:
                if production[0] != '\'' and production[0] != '\\':
                    split_production = production.split('.')
                    Last_production_symbol = split_production[len(split_production)-1]
                    for s in split_production:
                        epsilon_exists = 0
                        if s[0] != "'":
                            ###
                            # print('s',s)
                            nonterminal = get_nonterminal(s)
                            # print(nonterminal.name)
                            new_first_set = nonterminal.calculate_first_set()
                            for first in new_first_set:
                                if first != epsilon:
                                    first[1] = production
                                    self.first_set.append(first)
                                else:
                                    epsilon_exists = 1
                            # f for f in new_first_set if f not in self.first_set
                            if not epsilon_exists:
                                break
                            if s == Last_production_symbol:
                                self.first_set.append(epsilon)
                        else:
                            terminal = get_next_terminal(s) #ana shayfak bas fi
                            self.first_set.append([terminal, production])
                            break        
                else:
                    if production[0] == '\\':
                        self.first_set.append(epsilon)
                    else:
                        terminal = get_next_terminal(production)
                        self.first_set.append([terminal, production])
            
            self.is_first_calculated = 1
            return copy.deepcopy(self.first_set) 

    def calculate_follow_set(self):
        if self.is_start:
            self.follow_set.append('\'' + '$' + '\'')
        for production in self.production_set:
                split_production = production.split('.')
                production_length = len(split_production) 
                for i in range(production_length):
                    current_split_production = split_production[i]
                    if current_split_production[0] != '\'' and current_split_production[0] != '\\':
                        nonterminal = get_nonterminal(current_split_production)
                        if i == production_length - 1 and nonterminal.name != self.name and self.name not in nonterminal.follow_set:
                            nonterminal.follow_set.append(self.name)
                            break
                        for j in range(i+1, production_length):
                            next_split_production = split_production[j]
                            epsilon_exists = 0
                            if next_split_production[0] != '\'':
                                next_nonterminal = get_nonterminal(next_split_production)
                                new_first_set = next_nonterminal.calculate_first_set()
                                for first in new_first_set:
                                    if first != epsilon and '\'' + first[0] + '\'' not in nonterminal.follow_set:
                                        nonterminal.follow_set.append('\'' + first[0] + '\'')
                                    else:
                                        epsilon_exists = 1
                                if not epsilon_exists:
                                    break

                                if j == production_length - 1 and nonterminal.name != self.name and self.name not in nonterminal.follow_set:
                                    nonterminal.follow_set.append(self.name)
                            
                            else:
                                terminal = get_next_terminal(next_split_production)
                                if '\'' + terminal + '\'' not in nonterminal.follow_set:
                                    nonterminal.follow_set.append('\'' + terminal + '\'')
                                break

    def get_terminals(self):
        temp = []
        for production in self.production_set:
            if production != epsilon:
                temp = production.split('.')
                for term in temp:
                    if term[0]=="'":
                        terminal = get_next_terminal(term)
                        if terminal not in terminals:
                            terminals.append(terminal)

    def print_nonterminal(self):
        print(self.name, self.production_set)

    def print_nonterminal(self):
        print(self.name, self.production_set)


def substitute_follow_set():
    nonterminals_length = len(nonterminals)
    for i in range(nonterminals_length):
        current_nonterminal = nonterminals[i]
        for j in range(nonterminals_length):
            if j == i:
                continue
            else:
                if current_nonterminal.name in nonterminals[j].follow_set:
                    # print('BBBBBBBBBBBBBB',current_nonterminal.name)
                    nonterminals[j].follow_set.remove(current_nonterminal.name)
                    nonterminals[j].follow_set.extend(f for f in current_nonterminal.follow_set if f not in nonterminals[j].follow_set
                    and nonterminals[j].name != f)

def read_grammar_file():
    # grammar_file = open("input_CFG_LL.txt", "r")
    # grammar = grammar_file.read().split('\n')
    for grammar_line in records:
        grammar_line = re.sub('[ \t]', '.', grammar_line.mickey.strip())
        print(grammar_line)
        grammar_line = grammar_line.split('=', maxsplit=1)
        nonterminal_name = grammar_line[0]
        rules = grammar_line[1]
        
        new_nonterminal = nonTerminal_symbol(nonterminal_name)
        rules = rules.split('|')
        for rule in rules:
            new_nonterminal.production_set.append(rule)
        nonterminals.append(new_nonterminal)

    nonterminals[0].is_start = 1

    # for nonterminal in nonterminals:
    #     print(nonterminal.name)
    # print('*********************')



    for nonterminal in nonterminals:
        nonterminal.calculate_first_set()
        nonterminal.calculate_follow_set()
        nonterminal.get_terminals()


    # terminals.append('$')

    print('*********************')

    substitute_follow_set()

    print('*********************')
    print('first')
    for nonterminal in nonterminals:
        print(nonterminal.name,'-->', nonterminal.first_set)

    print('*********************')  
    print('follow')
    for nonterminal in nonterminals:
        print(nonterminal.name,'-->', nonterminal.follow_set)
    print('*********************')  

############################################################################################################################################

parsing_table = defaultdict(lambda x = None : x)
def create_table():

    for i in nonterminals:
        
        contains_eps = False
        for j in i.first_set:
            if j == epsilon :
                contains_eps = True
            else :
                if parsing_table[i.name + " " + j[0] ]:
                    print("ambiguous")
                else:
                    
                    parsing_table.update({ i.name + " " + j[0] : j[1] })

                
        
        for j in i.follow_set:
            if parsing_table[i.name + " " + get_next_terminal(j)]:
                k = 0
                # print("ambiguous",i.name + " " + get_next_terminal(j), parsing_table[i.name + " " + get_next_terminal(j)], (lambda : (sync,epsilon) [contains_eps])())
            else:
                parsing_table.update({ i.name + " " + get_next_terminal(j) : (lambda : (sync,epsilon) [contains_eps])() })


#############################################################################################################################################
def abkar():
    #######
    print(parsing_table)
    #terminals = ['id', '+', '*', '(', ')', '$']
    
    f = open("output.txt", "r")
    z=f.read()
    f.close()
    z = z + "\n"+"$"
    input = z.split() 
    top_stack = nonterminals[0].name
    print(input)
    # input = "id + id $".split()
    stack = []
    stack.append("$")
    stack.append(top_stack)
    
    production_output = ""
    str_t=""
    #first_input = input[0]
    matched = []
    j=0

    while(True):
       
        key = stack[-1] + " " + input[j]
        print(key)
        # error checking 2: if non terminal and key isnt in table
        if(key in parsing_table):
            #print("yes",key)
        # print(key)
            production = parsing_table[key].split('.')
            
        else:
            #panik mode recovery
            print("error :panick mode", str_t, production_output)
            #break
            while(True):
                if(key not in parsing_table):
                    j = j + 1
                    key = stack[-1] + " " + input[j]
                    # print('ssssssssssssssssss',key)
                elif(parsing_table[key].split('.') is sync):
                    stack.pop()
                    key = stack[-1] + " " + input[j]
                    print("sync")
                    #break
                else:
                    production = parsing_table[key].split('.')
                    print("production")
                    break

                
        
        for t in production:
            str_t = str_t + " " + t

        production_output = production_output +  stack[-1]+ " -->" + str_t + "\n"
        str_t=""
        production.reverse()
        stack.pop()
    
        #rev_production=production.reverse()
        
        #print(production)
        
        print("stack",stack)
        for i in production:
            if(i != epsilon):
                if i[0] == '\'':
                    i = get_next_terminal(i)
                if i != sync:
                    stack.append(i)
        # print("stack",stack)
        if(len(stack) == 1):
            break
        ## error checking 1: if stack[-1] is terminal != input[j] : error unmatched
        while(stack[-1] in terminals):
            
    
            if(stack[-1] == input[j] ):
            
                matched.append(stack[-1])
                print("matched",matched,)
                stack.pop()
                j = j + 1
                # production_output = production_output + "\n"
            else:
                print("error : insert",stack[-1])
                stack.pop()
                # production_output = production_output + "\n"
            
        
        top_stack = stack[-1]



    w = open("production_output.txt", "w")
    w.write(production_output)
    w.close()

def read_token_file():
      f = open('tokens.txt', 'r')
      terminals = f.read().split('\n')
    #   print(terminals)
      return terminals




read_grammar_file()
# terminals = read_token_file()
print('terminals:',terminals)
create_table()
print(parsing_table)
abkar()


#| 'addop'.TERM.SIMPLE_EXPRESSION_dash |\L