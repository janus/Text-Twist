import os
from string import find

currentdir = os.path.curdir
alphabet_dict = {'a':1, 'b':1, 'c':1, 'd':1, 'e':1, 'f':3, 'g':3, 'h':2, 'i':1, 'j':4, 'k':2, 'l':1, 'm':4, 'n':5, 'o':1, 'p':2, 'q':9, 'r':4, 's':2, 't':3, 'u':8, 'v':9, 'w':8, 'x':7, 'y':5, 'z':9 }
masterlist = []
word_list = []
searchwordlist = []

def cmp_count(word, given_tree):
     tree = make_tree(word)
     for l in tree:
          if tree[l] > given_tree[l]:
               return False
     return True
     
def make_tree(word):
     tree = {}.fromkeys(word, 0)
     for l in word: tree[l] +=1
     return tree

masterpath = os.path.join(currentdir, "bb")
masterpath = os.path.join(masterpath, "brit-a-z.txt")
def start_up():
     wordnlist = open(masterpath ,'r')
     temp_list = []
     mycount = 0
     for wordn in wordnlist:
       wordn = wordn.strip()
       if len(wordn) > 2 and len(wordn) < 14 :
          temp_list.append(wordn )
          if mycount == 20:
            sub_list =  temp_list[:]
            word_list.append(sub_list)
            sub_list, mycount, temp_list  = ([], 0, [])
       mycount = mycount + 1            
       if len(wordn) > 4 and len(wordn) < 14:
          masterlist.append(wordn)
     if temp_list:
         word_list.append(temp_list)

start_up()

def processed (my_tree, my_word):
        return ([], [].append(my_word))[cmp_count(my_word, my_tree)]

             
def update_searchlist(wordi):
     #search_path = os.path.join(list_path, wordi)
      global searchwordlist 
      tree = make_tree(wordi)
      given_letters = frozenset(wordi)
      searchwordlist = sum([ processed(tree, wordn)  for sub_list in word_list for wordn  in sub_list if given_letters.issuperset(frozenset(wordn)) ], [])


searchedwordset = set()
score_value = 0

def weight_sum( target_word):
         return sum([ alphabet_dict[v] for v in target_word])
         
def compute_result(downmessage):
         global score_value
        # global 
         message_str = "".join(downmessage)
         one_index = message_str.index("1") if "1" in message_str else len(message_str)
         target_str = message_str[:one_index]
         #print target_str
         if target_str in searchwordlist:
                 if target_str in searchedwordset:
                    return -1
                 else:
                    score_value = score_value + weight_sum(target_str)
                    searchedwordset.update([target_str])
                    return score_value
         else:
                    return -2
                    
def word_not_found(word):
      return  word not in searchedwordset:


