import _thread
import random
import time
from constants import timeout_lower, process_states


class Process:
	def __init__(self, process_id, state, timeout_upper = 5):
		"""
			args: 
				process_id: f'P{process_id + 1}'
				State: 					(HELD, WANTED, and DO-NOT-WANT) default: DO-NOT-WANT
				timestamp: 				Lamport timestamp. Default 0
		 		timeout-upper-bound: 	default 5
		"""
		self.id = process_id
		self.state = state
		self.timeout_upper = timeout_upper
		self.timer = None

	def __str__(self):
		return f"{self.id}, {process_states[self.state]}"

	__repr__ = __str__

	def start(self, conn):
		_thread.start_new_thread(self.run, (conn,))

	def run(self, conn):
		"""
			Run background Tasks for process.
			
			1. Get new Timeout length
			2. check state and decide tasks to be performed accordingly.
			3. Update timer in loop and then Change state after timing out
		"""
		while True:
			timeout = random.randint(timeout_lower, self.timeout_upper)
			self.timer = timeout
			if self.state == "want":
				schedule_work = conn.request_critical_section()
				if schedule_work:
					success = conn.access_critical_section()
					# print(f"{self.id} is attempting taking over Critical Section.")
					if success:
						# print(f"{self.id} is holding Critical Section.")
						self.set_state("held")
					else:
						# print(f"{self.id}:: Failed to access Critical Section")
						...
				# TODO: Remove empty else cases and print Statements after development.
				else:
					# print(f"{self.id}:: Failed to access Critical Section")
					...
			while self.timer:
				self.countdown()
			self.change_state()

	"""
		Timeout manipulation and Timer support methods 
	"""

	def set_timeout_upper(self, timeout_upper):
		self.timeout_upper = max(timeout_upper, timeout_lower)

	def countdown(self):
		time.sleep(1)
		self.timer -= 1

	def get_timestamp(self):
		return time.monotonic()



	"""
		getter and setter calls
	"""

	def set_state(self, state):
		self.state = state

	def get_state(self):
		return self.__str__()

	def change_state(self):
		if self.state != "held":
			self.set_state(random.choice(["want", "do_not_want"]))

	def release_critical_section(self):
		self.set_state("do_not_want")
