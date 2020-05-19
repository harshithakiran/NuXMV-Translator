"""
Author: Harshitha Kiran
Email: hkiran2014@my.fit.edu
Created during summer of 2020
"""
from typing import List
import nltk as nltk
from nltk import word_tokenize
from nltk import pos_tag
from nltk import RegexpParser
import translate
import re
# if ^Variable that preeceds would be attached state_^variable
# <s> or state that would have value 'state'
# extract modules, var, vlaues, attributes

with open('Read_ruleone.soar') as input_file:
    tokens_str = input_file.read().replace('\n', '');  # print("string tokens-->", tokens_str)

translationDictionary_forProposeInitialize = {  # key:value
    '(state': 'state_',
    '<s': 'state_',
    'nil': 'nil',
    '(<s>': 'state',
    '<o>': 'state_operator',
    '+)(<o>': 'state_operator'
}

class Translate:

    # getting individual soar items
    def extractionsForTranslation(tokens_str):
        global remaining_string, remaining_string_toList, module, attributes
        attributes = []
        list_states = []
        list_values = []
        getVariables = []  # states+attributes

        module = tokens_str[0:4]  # stripping sp from main str
        stripping_sp = tokens_str.split(module)
        remaining_string= str(stripping_sp).strip('[]').replace("'', '", '')  # remaining str every time after stripping sp
        remaining_string_toList = re.sub("/^[ A-Za-z0-9()[]+-*/%]*$/", " ", remaining_string).split()
        print("module extracted", module, "\nextractions remaining:\n", remaining_string, "\n", remaining_string_toList)

        for i in remaining_string_toList:
            if str(i).startswith("^"): attributes.append(str(i))  # get attributes
            if (i in translationDictionary_forProposeInitialize.keys()):
                list_states.append(translationDictionary_forProposeInitialize[i])

        list_states = list(dict.fromkeys(list_states))
        attributes = list(dict.fromkeys(attributes))
        print(" \n extracting state operators before attributes: \n states extracted", list_states, "\n Attributes extracted:", attributes)
        for j in attributes:
            beforeAttribute = remaining_string.partition(str(j))  # -->here, extracting fullstr before attributes
        print(beforeAttribute)

    def conditions_actions(remaining_string):
        global rhs_Str, lhs_Str
        rhs_Str= re.sub(r'^.*?-->', '', remaining_string)  # str datastruc. remove everything before -->

        lhs_str = remaining_string.split("-->", 1)[0]  # list datatstruc. split once on -->,get only first elementon list
        lhs_Str=str(lhs_str)
        print("\nConditions & Actions \nLHS\n", lhs_Str,"\nRHS\n", str(rhs_Str))


    def match_variables(lhs_Str,rhs_Str):
        lhs_Str_list=lhs_Str.split(" ") # str to list
        rhs_Str_list = rhs_Str.split(" ")
        lhs_res = {key: translationDictionary_forProposeInitialize[key] for key in translationDictionary_forProposeInitialize.keys()
           & {'(state', '<s'}} # extracting specific keys
        print(str(lhs_res))

        def replace_last(source_string, replace_what, replace_with):
            head, _sep, tail = source_string.rpartition(replace_what)
            return head + replace_with + tail
        state_ = replace_last(lhs_Str, "(state <s>", "state_") # str
        state_ = re.sub(r'^.*? ', '', state_) #remove everything before state
        only_state = str(state_.split()[0])
        print("state_\n",state_.rstrip(" "), "\nonly state\n",only_state)

        after_state= lhs_Str.split('>')[1].lstrip().split(''',[], ''') # list having only one item
        after_state="".join(after_state) # now str
        print("after_state\n",after_state.strip(')')) #strip on str to remove ) not WORKING?????????????????????????????????????????????

        after_state_list = after_state.split(" ")
        after_state_list=after_state_list[:-1] # removes last element of list
        if("nil)" in after_state_list): after_state_list.remove("nil)")
        print("after_state_list\n", after_state_list)

        for i in after_state_list:
            j = "VAR " + only_state + str(i)
            print(j)

        def getRHS():
            state_=replace_last(rhs_Str,"(state <s>", "state_")
            state_ = re.sub(r'^.*? ', '', state_)  # remove everything before state
            only_state = str(state_.split()[0])
            after_state = rhs_Str.split('>')[1].lstrip().split(''',[], ''')  # list having only one item
            after_state = "".join(after_state)  # now str
            after_state_list = after_state.split(" ")
            for i in after_state_list:
                j = "VAR " + only_state + str(i)
                print(j)


        getRHS()







    extractionsForTranslation(tokens_str)
    conditions_actions(remaining_string)
    match_variables(lhs_Str, rhs_Str)



