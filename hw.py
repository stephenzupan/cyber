#!/usr/bin/python

import socket
import threading
import random
import os
import time
import subprocess

PORT = 12345
DEBUG = False
TIME = time.time()
RANDOMS = 0


SPONGEBOB = " \
      .--..--..--..--..--..-.                 \n\
    .' \  (`._   (_)     _   \                \n\
  .'    |  '._)         (_)  |                \n\
  \ _.')\      .----..---.   /                \n\
  |(_.'  |    /    .-\-.  \  |                \n\
  \     0|    |   ( O| O) | o|                \n\
   |  _  |  .--.____.'._.-.  |                \n\
   \ (_) | o         -` .-`  |                \n\
    |    \   |`-._ _ _ _ _\ /                 \n\
    \    |   |  `. |_||_|   |                 \n\
    | o  |    \_      \     |     -.   .-.    \n\
    |.-.  \     `--..-'   O |     `.`-' .'    \n\
  _.'  .' |     `-.-'      /-.__   ' .-'      \n\
.' `-.` '.|='=.='=.='=.='=|._/_ `-'.'         \n\
`-._  `.  |________/\_____|    `-.'           \n\
   .'   ).| '=' '='\/ '=' |                   \n\
   `._.`  '---------------'                   \n\
         //___\   //___\                      \n\
           ||       ||                        \n\
           ||_.-.   ||_.-.                    \n\
          (_.--__) (_.--__)                   \n\
"

SQUIDWARD = "                       \n\
           .--'''''''''--.          \n\
        .'      .---.      '.       \n\
       /    .-----------.    \      \n\
      /        .-----.        \     \n\
      |       .-.   .-.       |     \n\
      |      /   \ /   \      |     \n\
       \    | .-. | .-. |    /      \n\
        '-._| | | | | | |_.-'       \n\
            | '-' | '-' |           \n\
             \___/ \___/            \n\
          _.-'  /   \  `-._         \n\
        .' _.--|     |--._ '.       \n\
        ' _...-|     |-..._ '       \n\
               |     |              \n\
               '.___.'              \n\
                 | |                \n\
                _| |_               \n\
               /\( )/\              \n\
              /  ` '  \             \n\
             | |     | |            \n\
             '-'     '-'            \n\
             | |     | |            \n\
             | |     | |            \n\
             | |-----| |            \n\
          .`/  |     | |/`.         \n\
          |    |     |    |         \n\
          '._.'| .-. |'._.'         \n\
                \ | /               \n\
                | | |               \n\
                | | |               \n\
                | | |               \n\
               /| | |\              \n\
             .'_| | |_`.            \n\
             `. | | | .'            \n\
          .    /  |  \    .         \n\
         /o`.-'  / \  `-.`o\        \n\
        /o  o\ .'   `. /o  o\       \n\
        `.___.'       `.___.'       \n\
"                      
# Helper method to send
def send(conn, string):
	conn.send(string)
	time.sleep(.05)


# Helper Method
# returns the alphanumeric characters of a string (a-z, 0-9, A-Z)
def alnum(string):
	return ''.join(ch for ch in string if ch.isalnum())


# Random Integer generator
# Generates a random number from 1 to max.
def randInt(maximum):
	global RANDOMS
	RANDOMS += 1
	return (int)(random.random() * maximum + 1)


# Helper Method
# Generates a random pin.
def randPin(size):
	global RANDOMS
	RANDOMS += 1
	return str((int)(random.random() * 10 ** size)).zfill(size)


# Helper Method
# Prints a debug message if the DEBUG flag is set.
def dbg_print(msg):
	if DEBUG:
		print(msg)

# Squidward validation
def option1(conn, pin):
	seed = randPin(10)
	if seed == pin:
		seed = randPin(10)
	i = 0

	for char in SQUIDWARD:
		send(conn, "Please enter validation key:\n")
		key = conn.recv(8192).strip()
		if (key[i] % ord(char)) + ord(char) - 1 == char:
			send(conn, SQUIDWARD)
			newchar = conn.recv(1)
			# set first char of seed
			seed = newchar + seed[1:]
		elif key == SPONGEBOB:
			send(conn, "Please enter padding:\n")
			padding = conn.recv(8192)
			if padding == SQUIDWARD * 9:
				# Set last char of seed
				seed = seed[:-1] + "9"
				send(conn, "Padding set\n")
			elif padding == SQUIDWARD * 8:
				# Set last char of seed
				seed = seed[:-1] + "8"
				send(conn, "Padding set\n")
			elif padding == SQUIDWARD * 7:
				# Set last char of seed
				seed = seed[:-1] + "7"
				send(conn, "Padding set\n")
			elif padding == SQUIDWARD * 6:
				# Set last char of seed
				seed = seed[:-1] + "6"
				send(conn, "Padding set\n")
			elif padding == SQUIDWARD * 5:
				# Set last char of seed
				seed = seed[:-1] + "5"
				send(conn, "Padding set\n")
			elif padding == SQUIDWARD * 4:
				# Set last char of seed
				seed = seed[:-1] + "4"
				send(conn, "Padding set\n")
			elif padding == SQUIDWARD * 3:
				# Set last char of seed
				seed = seed[:-1] + "3"
				send(conn, "Padding set\n")
			elif padding == SQUIDWARD * 2:
				# Set last char of seed
				seed = seed[:-1] + "2"
				send(conn, "Padding set\n")
			elif padding == SQUIDWARD * 1:
				# Set last char of seed
				seed = seed[:-1] + "1"
				send(conn, "Padding set\n")
			elif padding == SQUIDWARD * 0:
				# Set last char of seed
				seed = seed[:-1] + "0"
				send(conn, "Padding set\n")
			else:
				send(conn, "Invalid padding\n")
		elif key == SQUIDWARD:
			seed = "0000000000"
		elif key == "mayonnaise":
			seed = seed[5:] + "3" + seed[:-4]
		elif key == "random!!":
			# Prevent brute forces
			send(conn, "Setting random pin...")
			seed = randPin(9)
		elif key == "op2":
			send(conn, "")
			character = conn.recv(1)
			key += character
			send(conn, "Char set!")
		else:
			send(conn, "Invalid key")
	if seed == pin:
		return False, True
	return False, False


# Informational header
def option2(conn):
	send(conn, SPONGEBOB)
	return False


# touch file
def option3(conn):
	send(conn, "Enter file to create \n")
	data = conn.recv(1024).strip()

	if os.getcwd() == '/trusted':
		# If run from a trusted directory, allow them to create any file
		out = subprocess.check_output("touch " + data, shell=True)
		send(conn, out)

	else:
		# Since not run from a trusted directory, check first
		os.system("touch " + alnum(data))
		send(conn, "Created file.")

	return False


# Sends number of times random has been called
def option4(conn):
	global RANDOMS
	send(conn, str(RANDOMS) + "\n")
	return False


# Get cwd
def option5(conn):
	send(conn, os.getcwd() + "\n")
	return False


# Sends examples of possible pins
def option6(conn):
	for i in range(10):
		send(conn, randPin(10) + "\n")
	return False

# Change directories. Only admins can change directories.
def option7(conn, admin):
	if admin:
		send(conn, "Enter target directory \n")
		data = conn.recv(1024).strip()

		if data[0] == '\\' or data[0] == '~' or data[0] == '/':
			return True
		else:
			os.chdir(data)
			send(conn, "Changing directory...\n")
			dbg_print(os.getcwd())
			return False
	else:
		send(conn, "Cannot change directories unless in Admin mode.\n")
		return False

# Generate pin of length n
def option8(conn):
	send(conn, "Please enter then length of the pin\n")
	num = int(conn.recv(1024))
	send(conn, randPin(num) + "\n")
	return False


# KoolKevin's Awesome idea to prevent brute force password attacks!
# Sets admin to true if the pin is correct.
def option9(conn, pin):

	send(conn, "Please enter your pin. \n")
	data = conn.recv(1024).strip()
	send(conn, "Verifying....\n")

	if(len(data) != len(pin)):
		send(conn, "Your pin is not the correct length.\n")
		return False

	else:
		# Correct length.
		i = 0

		while i < len(pin):

			# Go through the pin

			if pin[i] == data[i]:
				# User supplied the correct digit! Now wait to prevent brute-force attacks.
				time.sleep(1)

			else:
				# Incorrect pin.
				send(conn, "Your pin was incorrect.\n")
				time.sleep(.1)
				return False

			i += 1

	# If it made it here, the full password was correct!
	send(conn, "Your pin was correct!\n")
	return True


# Closes the connection
def option10(conn):
	send(conn, "It was nice having you. we're sad to see you go :(\n")
	conn.close()
	return True


def initSocket(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("0.0.0.0", port))
	s.listen(1000)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	return s

def serve(conn):

	admin = False
	done = False
	pin = randPin(10)
	option = randInt(10)
	dbg_print("The session's pin is: " + pin)
	
	while not done:

		try:
			send(conn, "Type 'y' to do option " + str(option) + "\n")
			data = conn.recv(1024).strip()

			if data == 'y':
				if option == 1:
					done, admin = option1(conn, pin)
				elif option == 2:
					done = option2(conn)
				elif option == 3:
					done = option3(conn)
				elif option == 4:
					admin = option4(conn)
				elif option == 5:
					done = option5(conn)
				elif option == 6:
					done = option6(conn)
				elif option == 7:
					done = option7(conn, admin)
				elif option == 8:
					done = option8(conn)
				elif option == 9:
					admin = option9(conn, pin)
				elif option == 10:
					done = option10(conn)
			option = randInt(10)
		
		except socket.error:
			done = True
		except Exception as e:
			print(e)
			option += 1


def __main__():
	try:
		print("Awaiting connections")
		s = initSocket(PORT)
		while True:
			conn, addr = s.accept()
			t = threading.Thread(target=serve, args=(conn,))
			t.start()
	except KeyboardInterrupt:
			print("Closing.")
			os._exit(1)


__main__()
