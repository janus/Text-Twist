from Tkinter import *
import string 
import os
import random
import time
import dictj
import itertools
import tkMessageBox
import sys

root = Tk()

letters = string.letters[ :26]   #Alphabets
lettersdict = dict(zip(letters, range(len(letters))))
# letters with their position in alphabets
upmessage = []

mycount,gameon, mastercount,timecount, masterlen, gamestatus = (0,0,0,0,0,0)
next_game = 0
freeze_timer = 0
now = 0
mynumber = 1

masterword = dictj.masterlist
#This hold the list of words we are going to twist
masterwordset = set(masterword)  #To make search easier
random.shuffle(masterword)
list_label,imagelist, list_label1, listimagephoto = ([],[],[],[])
score_label = []
currentdir = os.path.curdir
doom_image = os.path.join(currentdir, "doom2.gif")
IMAGE = PhotoImage(file=doom_image)  #'C:\Python_way\doom2.gif')
IMAGE_DIR = os.path.join(currentdir, "image") #C:\\Python_way\\image\\"

def nextword(n):
    "return a word from the master list"
    if n == masterlen:
       return masterword[0]
    return masterword[n]
     

wordi = nextword(mycount) #Initialize wordi
nlen =   len(wordi)

def init_list(val, length):
    return   [val for i in range(length)]
    
downmessage,statusdown,statusup =  ( init_list("1", nlen ) ,init_list(0,nlen), init_list(1,nlen))#list of characters clicked
#Setup up initial values for the lists that hold characters or status


class Message:
"This is a class with two important methods,the callbacks. It also has the re-start method"
    def performbind(self,  label, f):
          label.bind('<Button-1>', (lambda event : f(event)))  
#The row where characters must be before getting score. It is basically binding and unbinding.
    def acallback(self, event):
       "This is mainly acts to swap images and characters between the two rows"
       for i, label in enumerate(list_label1):
          if event.widget == label:
            statusdown[i] = 0
            for ind, val in enumerate(statusup):
                    if val == 0:
                       label.unbind('<Button-1>')
                       new_label = list_label[ind]
                       new_label["image"],new_label["text"] = (label["image"],label["text"])
                       downmessage[i ] , label["image"] = ("1" ,IMAGE)
                       upmessage[ind] = label["text"]
                       self.performbind( new_label, self.callback)
                       list_label[ind], list_label1[i], statusup[ind] = (new_label,label, 1)
                       break
            return 
#For the rwo with caharcters at the start of game        
    def callback(self,event):
         "This is mainly acts to swap images and characters between the two rows"      
         for i, label in enumerate(list_label):
            if event.widget == label:
               upmessage[i] = "1"
               statusup[i] = 0
               for inde, val in enumerate(statusdown):
                if val == 0:
                      label.unbind('<Button-1>')
                      change_label = list_label1[inde]
                      change_label["image"], change_label["text"], downmessage[inde] = (label["image"],label["text"],label["text"])
                      label["image"] = IMAGE
                      self.performbind(change_label,self.acallback)
                      list_label1[inde] , list_label[i],statusdown[inde]  = (change_label,label,1)
                      break
         return
     
    def perform_image_unbind(self, num, temp_data):
          "Helper method for removing an image bind"
          label = list_label[num]
          if temp_data[num] is not  "1":
              label.unbind('<Button-1>')
              label["image"],list_label[num] , statusup[num] = (IMAGE,label,0)
              
    def perform_image_bind(self, num, temp_data):
            "Helper method for adding an image bind"
            label = list_label[num]
            if temp_data[num] is not  "1":
               label["text"], label["image"] ,list_label[num]= (upmessage[num],create_image(upmessage[num]),label)
            else:
               label["image"], label["text"] =  (create_image(upmessage[num]) ,  upmessage[num]  )
               self.performbind(label,self.callback)
               list_label[num], statusup[num] = (label, 1)    
         
    def shuffle(self):
          "After shuffling we unbind and bind depending on where the image object falls" 
          temp = upmessage[:]
          random.shuffle(upmessage)
          for i, val in enumerate(upmessage):
               if val == "1":
                  self.perform_image_unbind(i, temp)
               else:
                  self.perform_image_bind(i, temp)
                 
    def char_tok(self,word_new):
          "Turn a word into a list of characters "
          for  cha in word_new:
                upmessage.append(cha)

    def my_make(self,data_store,element, num):
         "Update "
         temp = init_list(element, num)
         for x in temp:
             data_store.append(x)

    def  reset_inits(self, myword):
        "This resets the initials"
        del upmessage[:]
        self.char_tok(myword)
        mlen = len(myword)
        del downmessage[:]
        del statusdown[:]
        del statusup[:]
        self.my_make( downmessage, "1",mlen)
        self.my_make(statusdown, 0,mlen)
        self.my_make(statusup, 1,mlen)
        
      
    def get_score(self):
          "Score is pulled from dictj module"   
          resultvalue = dictj.compute_result(downmessage)
          score_value = dictj.score_value
          if -1 == resultvalue:
            tkMessageBox.showinfo("Have already seen","You have seen this word")
          elif -2 == resultvalue:
            tkMessageBox.showinfo("That is not in dictonary", "Your word is wrong")
          else:
                 score_label[0]["text"] = str(score_value)

    def remove_widgets(self, mylabel_list, myword):
        "Reseting widgets"
        for k, f in enumerate(myword):
           label  = mylabel_list[k]
           if IMAGE == label["image"]:
               label.grid_remove()
               mylabel_list[k] = label
           else:
              label.unbind('<Button-1>')
              label.grid_remove()
              mylabel_list[k] = label

#Update the GUI 
    def update_gui(self, new_word):
      "Update the GUI "
      global wordi
      self.remove_widgets(list_label, wordi)
      self.remove_widgets(list_label1, wordi)
      dictj.update_searchlist(new_word)
      my_word =    random.choice(list(map("".join, itertools.permutations(new_word))))
      for i,cha in enumerate(my_word):
        photoimage = create_image(cha)
        word_label = list_label[i]
        word_label["image"] ,word_label["text"] = (photoimage, cha)
        word_label.grid()
        word_label.bind('<Button-1>', (lambda event : self.callback(event)))
        list_label[i] , empty_label = (word_label, list_label1[i])
        empty_label["image"] = IMAGE
        empty_label.grid()
        list_label1[i] = empty_label
      wordi = my_word
      dictj.searchedwordset = set()
    

    def restart_game(self):
         "Re-starting game all over again"    
         global mastercount
         global freeze_timer
         random.shuffle(masterword)
         mastercount = 0
         dictj.score_value = 0
         self.update_gui(masterword[mastercount])
         score_label[0]["text"] = str(dictj.score_value)
         freeze_timer = 0

def create_image( cha):
      imagename = "cat%s.gif" % (lettersdict[cha] + 1)
      photoimage = PhotoImage(file=os.path.join(IMAGE_DIR , imagename))
      listimagephoto.append(photoimage)
      return photoimage
      
# This is where the gui is created and all the artifacts
      
def create_gui():
     "This is where the gui is created and all the other artifacts"
     global wordi
     global mynumber
     global mastercount
     global freeze_timer
     global next_game
     if 1 == mynumber:
       mynumber = 0
       dictj.update_searchlist(wordi)
       wordi  =     random.choice(list(map("".join, itertools.permutations(wordi))))
       for i,cha in enumerate(wordi):
        photoimage = create_image(cha)
        upmessage.append(cha)
        label = Label(root,  image=photoimage, text = cha)
        label.grid(row=1, column=i, columnspan=1, rowspan=1,sticky=W+E+N+S, padx=0, pady=1)
        label1 = Label(root,  image=IMAGE)
        label1.grid(row=0, column=i, columnspan=1, rowspan=1,sticky=W+E+N+S, padx=0, pady=1)
        label_object = Message()
        label.bind('<Button-1>', (lambda event : label_object.callback(event)))
        list_label.append(label)
        list_label1.append(label1)
       for k in range(14)[len(wordi):]:
        label = Label(root,  image=IMAGE)
        label.grid(row=1, column=k, columnspan=1, rowspan=1,sticky=W+E+N+S, padx=0, pady=1)
        label1 = Label(root,  image=IMAGE)
        label1.grid(row=0, column=k, columnspan=1, rowspan=1,sticky=W+E+N+S, padx=0, pady=1)
        label.grid_remove()
        label1.grid_remove()
        list_label.append(label)
        list_label1.append(label1)
       button_object = Message() 
       Label(root, text="Time:").grid(row=5,column=0, columnspan=1, rowspan=1)
       update_clock()
       button_shuffle = Button(root, text="Shuffle", command=button_object .shuffle)
       button_shuffle.grid(row=4, column=2, columnspan=2)
       button_check = Button(root, text="Check Out", command=button_object .get_score)
       button_check .grid(row=4, column=8, columnspan=2)
       Label(root, text="Score:").grid(row=0,column=20, columnspan=1, rowspan=1)
       scorelabel = Label(root, text = 0)
       scorelabel.grid(row=1, column=20, columnspan=1, rowspan=1)
       score_label.append(scorelabel) 
     else:
       gui_object = Message()
       if dictj.word_not_found(masterword[mastercount]) and next_game == 0:
          freeze_timer = 1
          your_decision = tkMessageBox.askyesno( "Decision time" , "Do you want to continue?" )
          if your_decision is True:
                gui_object.restart_game()
          else:
                sys.exit()     
       next_game = 0
       mastercount = mastercount  + 1
       gui_object.reset_inits(masterword[mastercount])
       gui_object.update_gui(masterword[mastercount])
       root.bell()
     root.after(120000, create_gui)
     root.geometry("400x200")
     root.mainloop()

def update_clock():
    "This generates the time used to update to next level"
    global now
    global timecount
    if freeze_timer == 0:
        if timecount  < 60:
            now = "0:%d" % timecount
            timecount = timecount + 1
        elif timecount >= 60 and timecount < 120:
           gnum = timecount%60
           now = "1:%d" % gnum
           timecount = timecount + 1
        else:
          now = "2:00"
          timecount = 0
    else:    
          pass
    Label(root, text=now).grid(row=6,column=0, columnspan=1, rowspan=1)
    root.after(1000, update_clock)
  
def main():
      dictj.start_up()
      create_gui()

if __name__=='__main__':
    main()
   
     
