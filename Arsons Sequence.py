import re as r
from num2words import num2words as n
#Arson's Sequence

string = "T is the first, fourth, eleventh, sixteenth, ... letter in this sentence."

def Scanner(ini_string):
    zapple = r.findall(r'[\w]?', ini_string)
    newlist = [x for x in zapple if x != '']
    lists = []
    lists2 = []
    lists3 = []
    i = 0
    for x in newlist:
        i += 1  
        lists.append(i)
        lists2.append(x)
    lst_tuple = list(zip(lists,lists2))
    lists3 = [n(x[0], to='ordinal') for x in lst_tuple if 't' in x or 'T' in x]
    return lists3


def StringReplacer(string_to_replace, list1, list2): 
        for item in list1:
            if item not in list2:
                    list2.append(item)
                    string_to_replace = string_to_replace.replace("...", item + ", ...")
                    return string_to_replace

                
lists6 = ['first', 'fourth', 'eleventh', 'sixteenth']


for x in range(20):
    newstring = StringReplacer(string, Scanner(string), lists6)
    string = StringReplacer(newstring, Scanner(newstring), lists6)
    

    

print(string)








            
        
#take all numbers, convert to ordinals, for each item in list search string if not there add, first count would be replace    

