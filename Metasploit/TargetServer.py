import socket
import subprocess
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 3285))
s.listen(1000)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def interpret(conn):
	while True:
		try:
			data = conn.recv(1024).strip()
			out = subprocess.check_output("python -c \"" + data + "\"", shell=True)
			conn.sendall(str(out))
		except Exception as e:
			conn.sendall(str(e))
			conn.sendall('\n')
def serve(conn):
	
	yesed = False
	viewed = False
	try:
		while True:
			if yesed == False:
				conn.sendall("Welcome to BockServe 2.0a! Please type 'yes' to agree to the terms and conditions, or 'view' to view the terms and conditions.\n")
			
				data = conn.recv(1024)
				if 'view' in data:
					conn.sendall("This service is operated by BockManity. Throughout the service, the terms \"we\", \"us\", and \"our\" refer to BockManity. BockManity offers this service, BockServe, including all information, tools, and services available from this site to you. Please read these terms and conditions, including those additional terms and conditions and policies referenced herein. Those Terms of Service apply to all users of the site, including without limitation users who are browsers, vendors, customers, merchants, and/or contributors of content. \n\n Please read these Terms of Service carefully before accessing or using our website. By accessing or using any part of the site, you agree to be bound by these Terms of Service.\n\n Any new features or tools which are added to the current store shall also be subject to the Terms of Service. You can review the most current version of the Terms of Service any time here. We reserve the right to update, change, or replace any of these Terms of Service by posting updates and/or changes here. It is your responsibility to check this page periodically for changes. \n\n")
					viewed = True
				elif 'yes' in data:
					if viewed == False:
						conn.sendall("Please view the terms and conditions before using BockServe 2.0.\n")
					else:	
						conn.sendall("Thank you for agreeing to the terms and conditions. BockServe 2.0 will now allow you to send any input and it will now interpret your input.\n")	
						yesed = True	
						interpret(conn)
						return
			else:
				interpret(conn)
				return
	except Exception as e:
		print e

while True:
	conn, addr = s.accept()
	t = threading.Thread(target = serve, args=(conn,))
	t.start()
