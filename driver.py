import sys
import rpyc
import datetime
from rpyc.utils.server import ThreadedServer

date_time = datetime.datetime.now()

connections = []

def handle_remote_command(command_args):
	remote_command = command_args[0]
	if len(command_args) > 3:
		print("Too many arguments")

	# handle exit
	elif remote_command == "exit":
		print("Exiting program")
		# TODO: kill process threads
		sys.exit(0)
	# handle list
	elif remote_command == "list":
		try:
			# TODO: List Processes along with their status
			for connection in connections:
				print(connection.root.get_state())
		except Exception as E:
			print("Error: ", E)

	# handle clock
	elif remote_command == "time-cs":
		try:
			if len(command_args) != 2 or not command_args[1].isdigit():
				print("Usage: 'time-cs <time(seconds)>'")
			else:
				...
				# TODO: Handle time-cs  
					# args: command_args[1] - Timeout for critical section
		except:
			print("Error")

	# handle clock
	elif remote_command == "time-p":
		try:
			if len(command_args) != 2 or not command_args[1].isdigit():
				print("Usage: 'time-p <time(seconds)>'")
			else:
				for connection in connections:
					connection.root.set_timeout_upper(int(command_args[1]))
		except:
			print("Error")

	# handle unsupported command        
	else:
		print("Unsupported command:", remote_command)


class ClientService(rpyc.Service):
	def on_connect(self, conn):
		self._conn = conn
		print("\nconnected on {}".format(date_time))

	def exposed_request_access(self, external_timestamp):
		flag = True
		# TODO: Ask other connenctions for CS with own timestamp
		for connection in connections:
			if connection != self._conn:
				flag = flag and connection.root.get_callback(external_timestamp)
		if flag:
			return True
		else: 
			return False

	def on_disconnect(self, conn):  
		print("disconnected on {}\n".format(date_time))


def initialize_connections(process_count):
	for process_id in range(process_count):
		conn = rpyc.connect("localhost", 18812, service = ClientService)
		conn.root.init_process(f"P{process_id + 1}", "do_not_want")
		print(f"Process P{process_id + 1} initialized")
		connections.append(conn)


	# TODO: Critical Section
	# Instantiate Critical Section.
		# args: state: HELD or Available
		# 		Held by: Process_id
		# 		timeout-lower-bound: fixed 10
		# 		timeout-upper-bound: default 10

if __name__=='__main__':
	
	if len(sys.argv) > 1:
		if int(sys.argv[1]) > 0:
			initialize_connections(int(sys.argv[1]))
		else:
			print("No of connections cannot be less than 1.")
			sys.exit(0)
	else:
		print("Usage: 'driver_service.py <number_of_connections>'")
		sys.exit(0)

	while True:
		command = input("$ ")
		handle_remote_command(command.lower().split(" "))