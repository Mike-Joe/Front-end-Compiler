# import re
epsilon = '\L'

global iterator
iterator = 0
class record:
    def __init__(self, nonterminal ,definition ) -> None:
        self.nonterminal = nonterminal
        self.definition = definition

def read_file(file_name = "input_CFG_LL.txt"):
    records = []
    f = open(file_name, 'r', encoding='windows-1252')
    lines0 = f.readlines()
    lines = []
    lines.append(lines0[0][1:])
    j = 0
    for i in range(1,len(lines0)):
        if lines0[i][0] == "#":
            j = i
            lines.append(lines0[i][1:])
        else:
            lines[j] = lines[j].strip('\n') + " " + lines0[i]

    for line in lines :
        # line = re.sub(r'[^\x00-\x7F]',"'", line)
        line = line.split('=', maxsplit=1)
        temp = record(line[0].strip() , line[1].strip())
        records.append(temp)
    return records

def merge(recor:record , factor:str , records , stupid_char ,concatination_symbol ):  
    global iterator
    new_name = recor.nonterminal+stupid_char+str(iterator)
    new_record = record(new_name,[])
    iterator+=1
    temp = [] 
    iter = 0 
    while (iter < len(recor.definition)):
        if recor.definition[iter] == factor:
            del recor.definition[iter]
            if epsilon not in temp:
                temp.append(epsilon)
            continue
        else:
            terms = recor.definition[iter].strip().split()
            if terms[0] == factor:
                # for i in range( 1 , len( terms ) ):
                #     if terms[i] not in temp:
                #         temp.append(terms[i])
                register = " ".join(terms[1:])
                if register not in temp:
                    temp.append(register)
                del recor.definition[iter] 
                continue
        iter +=1
    recor.definition.append(factor+concatination_symbol+new_name)
    new_record.definition = temp
    records.append(new_record)
        
def find_if_common(records, stupid_char = '#' ,concatination_symbol = ' '):
    for recor in records: 
        temp = []
        if "|" in recor.definition:
            recor.definition = [production.strip() for production in recor.definition.split('|')]
        if not isinstance(recor.definition, str):
            for term in recor.definition:  
                term = term.strip().split()
                if  not isinstance(term, str):  # includes concatinations
                    if term[0] in temp:
                        merge(recor,term[0],records, stupid_char , concatination_symbol )
                        find_if_common(records)
                        return records
                    else:
                        temp.append(term[0])


                else :                          # single term in production no concatinations
                    if term in temp:
                        merge(recor , term , records , stupid_char , concatination_symbol )
                        find_if_common()
                        return records
                    else :
                        temp.append(term)
    return records

def mickeyfy(records , or_symbol = "|" , mickey_concat_sym = "." ):
    for recor in records:
        if isinstance(recor.definition , str):
            definition_str = recor.definition
        else:
            definition_str = or_symbol.join(recor.definition).strip().replace(" ",".")
        recor.mickey = recor.nonterminal +"="+ definition_str
    return records

def main():
    records = read_file()
    find_if_common(records)

if __name__ == "__main__":
    main()

