from Tkinter import *
import numpy as np
import time
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
from threading import Thread
import random

options = [
	[2,'p'],
	[1,'q'],
	[2,'e'],
	[2,'r'],
	[1,'w'],
	[2,'t'],
	[1,'m'],
	[2,'o'],
	[2,'l'],
	[1,'d'],
	[1,'h',1],
	[1,'t',1],
	[1,'s',1],
	[1,'m',1],
	[1,'n',1],
	[1,'e',1,1],
	[1,'r',1,1],
	[1,'t',1,1],
	[1,'d',1,1],
	[1,'s',1,1],
	[1,'n',1,1],
	[1,'m',1,1]
	#[1,'r','d',1,1],
	#[1,'w','e',1,1],
	#[1,'q','t',1,1],
	#[1,'i','e',1,1],
	#[1,'a','l',1,1],
	#[1,'h','e',1,1],
	]

r = sr.Recognizer()
FS = 44100

root = Tk()



player1 = [0,0]
player2 = [0,0]

lst = [[0,0,0,0], 
       [0,0,0,0], 
       [0,0,0,0], 
       [0,0,0,0], 
       [0,0,0,0]]

turn = 1


entries = []

listening_entry = Entry(root, width = 30, fg = 'black',font=('Arial',16,'bold'))

word = ""
checking = 0

def draw_table():
	global player1, player2, turn, word, entries, listening_entry, lst, options, inds
	myLabel1 = Label(root, text = "P1 -- Player 1")
	myLabel2 = Label(root, text = "P2 -- Player 2")
	#myLabel_listen = Label(root, text = "Listening to Player ", pady = 10, padx = 20)

	myLabel1.grid(row = 0, column = 0)
	myLabel2.grid(row = 1, column = 0)
	listening_entry.grid(row = 2, column = 0)


	for i in range(len(lst)):
		entries.append([])
		for j in range(len(lst[0])):
			entries[i].append(Entry(root, width = 15, fg = 'blue',font=('Arial',16,'bold')))
			entries[i][j].grid(row = i, column = j + 3)
			if (player1[0] == i and player1[1] == j):
				#entries[i][j].configure(fg = 'red')
				entries[i][j].insert(0, " P1 ")
				#entries[i][j].configure(fg = 'blue')
			if (player2[0] == i and player2[1] == j):
				entries[i][j].insert(0, " P2 ")



def show_constraints():
	global player1, player2, turn, word, entries, listening_entry, lst, options, inds
	def helper(i, j, rd):
		global player1, player2, turn, word, entries, listening_entry, lst, options, inds
		if len(options[rd]) == 2:
			entries[i][j].insert(END, str(options[rd][0]) + " - " + str(options[rd][1]))
		if len(options[rd]) == 3:
			entries[i][j].insert(END, " start with " + str(options[rd][1]))
		if len(options[rd]) == 4:
			entries[i][j].insert(END, " end with " + str(options[rd][1]))
		if len(options[rd]) == 5:
			entries[i][j].insert(END, " start with " + str(options[rd][1]) + " end with " + str(options[rd][2]))


	ans = []
	player = player1
	if (turn == 2):
		player = player2
	rand = random.sample(range(0, len(options)), 3)
	rd1 = rand[0]
	rd2 = rand[1]
	rd3 = rand[2]
	if (player[1] != len(lst[0]) - 1):
		#rd1 = randrange(len(options))
		ans.append(rd1)
		helper(player[0], player[1] + 1, rd1)

	if (player[0] != len(lst) - 1 and player[1] != len(lst[0]) - 1):
		#while (rd2 == rd1):
		#	rd2 = randrange(len(options))
		ans.append(rd2)
		helper(player[0] + 1, player[1] + 1, rd2)

	if (player[0] != len(lst) - 1):
		#while (rd3 == rd1 or rd3 == rd2):
		#	rd3 = randrange(len(options))
		ans.append(rd3)
		helper(player[0] + 1, player[1], rd3)

	return ans;


def move_player(i, j, opts, word1):
	global player1, player2, turn, entries, listening_entry, lst, options, inds
	def move(i, j, a, b):
		global player1, player2, turn, entries, listening_entry, lst, options, inds

		if (turn == 1):
			entries[a][b].insert(0, " P1 ")
			player1[0] = a
			player1[1] = b
		else:
			entries[a][b].insert(0, " P2 ")
			player2[0] = a
			player2[1] = b

	def check_matching(opt, word1):
		global player1, player2, turn, entries, listening_entry, lst, options, inds
		if len(options[opt]) == 2:
			t = 0
			for k in word1:
				if k == options[opt][1]:
					t = t + 1
			if t == options[opt][0]:
				return True
			return False
		if len(options[opt]) == 3:
			if word1[0].upper() == options[opt][1].upper():
				return True
			return False
		if len(options[opt]) == 4:
			if len(word1) > 0 and word1[len(word)-1].upper() == options[opt][1].upper():
				return True
			return False
		if len(options[opt]) == 5:
			if word1[0].upper() == options[opt][1].upper() and len(word1) > 0 and word1[len(word)-1].upper() == options[opt][2].upper():
				return True
			return False


	another_pl = player2
	if (turn == 2):
		another_pl = player1

	entries[i][j].delete(0, END)
	if (another_pl[0] == i and another_pl[1] == j):
		if (turn == 1):
			entries[i][j].insert(0, " P2 ")
		else:
			entries[i][j].insert(0, " P1 ")

	if (j != len(lst[0]) - 1):
		entries[i][j + 1].delete(0, END)
		if (another_pl[0] == i and another_pl[1] == j + 1):
			if (turn == 1):
				entries[i][j + 1].insert(0, " P2 ")
			else:
				entries[i][j + 1].insert(0, " P1 ")
			

		if (i != len(lst) - 1):
			entries[i + 1][j + 1].delete(0, END)
			if (another_pl[0] == i + 1 and another_pl[1] == j + 1):
				if (turn == 1):
					entries[i + 1][j + 1].insert(0, " P2 ")
				else:
					entries[i + 1][j + 1].insert(0, " P1 ")

	if (i != len(lst) - 1):
		entries[i + 1][j].delete(0, END)
		if (another_pl[0] == i + 1 and another_pl[1] == j):
			if (turn == 1):
				entries[i + 1][j].insert(0, " P2 ")
			else:
				entries[i + 1][j].insert(0, " P1 ")

	if (len(opts) == 0):
		if (turn == 1):
			entries[i][j].insert(0, " P1 ")
		else:
			entries[i][j].insert(0, " P2 ")
		return
	ind = 0
	if (j != len(lst[0]) - 1):
		if check_matching(opts[ind], word1):
			move(i, j, i, j + 1)
			return

		ind = ind + 1

		if (i != len(lst) - 1):
			if check_matching(opts[ind], word1):
				move(i, j, i + 1, j + 1)
				return
			ind = ind + 1

	if (i != len(lst) - 1):
		if check_matching(opts[ind], word1):
			move(i, j, i + 1, j)
			return 

		ind = ind + 1
	if (turn == 1):
		entries[i][j].insert(END, " P1 ")
	else:
		entries[i][j].insert(END, " P2 ")

		

def speech_rec():
    global player1, player2, turn, word, entries, listening_entry, lst, options, inds
    listening_entry.delete(0, END)
    if (turn == 1):
        listening_entry.insert(0, "Listening to Player 1")
    else:
        listening_entry.insert(0, "Listening to Player 2")

    timer_entry = Entry(root, width = 30, fg = 'black')
    timer_entry.grid(row = 3, column = 0)

    def update(seconds):
    	global player1, player2, turn, word, entries, listening_entry, lst, options, inds
    	timer = '{:02d}'.format(seconds)
    	timer_entry.delete(0, END)
    	timer_entry.insert(0, "Time left: " + timer)
    	seconds -= 1;
    	if (seconds == -1):
    		return

    	root.after(1000, lambda: update(seconds))
    
    def SpeechRecognizer():
        global player1, player2, turn, word, entries, listening_entry, lst, options, inds
        try:
            myrecord = sd.rec(int(6*FS), channels = 2, samplerate = FS, blocking = True)
            sd.wait()
            sf.write("test.wav", myrecord, 44100)
            time.sleep(1)
            with sr.WavFile("test.wav") as source:
                audio = r.record(source)
            s = r.recognize_google(audio)
            word = s.partition(' ')[0]
            output = Entry(root, width = 20, fg = 'black',font=('Arial',15,))
            output.grid(row = 4, column = 0)
            output.insert(0, word)
        except:
            output = Entry(root, width = 20, fg = 'black',font=('Arial',15,))
            output.grid(row = 4, column = 0)
            output.insert(0, "Could not understand.")
    
    recognizer = Thread(target = SpeechRecognizer)
	
    T1 = Thread(target = lambda: update(10))
    
    T1.start()
    recognizer.start()


def Add_check():
	global player1, player2, turn, word, entries, listening_entry, lst, options, checking, inds
	s = word

	if checking > 0:
		if len(s) == 0:
			inds = []
		if (turn == 1):
			move_player(player1[0], player1[1],inds, s)
			turn = 2
		else:
			move_player(player2[0], player2[1],inds, s)
			turn = 1

	if (player1[0] == len(lst) - 1 and player1[1] == len(lst[0]) - 1):
		winner = Label(root, text = "PLAYER 1 won the game!", fg = 'red')
		winner.grid(row = len(lst) + 3, column = len(lst[0]) / 2 + 2)
		player1 = [0,0]
		player2 = [0,0]
		checking = 0
		return
	if (player2[0] == len(lst) - 1 and player2[1] == len(lst[0]) - 1):
		winner = Label(root, text = "PLAYER 2 won the game!", fg = 'red')
		winner.grid(row = len(lst) + 3, column = len(lst[0]) / 2 + 2)
		player1 = [0,0]
		player2 = [0,0]
		checking = 0
		return

	checking = checking + 1

	inds = show_constraints()

	speech_rec()
	root.after(11000, Add_check)

draw_table()
startbutton = Button(root, text = "START", command = Add_check)
startbutton.grid(row = len(lst) + 1, column = len(lst[0]) / 2 + 2)

root.mainloop()



