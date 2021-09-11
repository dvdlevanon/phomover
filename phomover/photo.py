import hashlib

class Photo:
	def __init__(self, file):
		self.file = file
		self.resolution_x = 0
		self.resolution_y = 0
		self.fingerprint = ""
	
	def get_id(self):
		return hashlib.md5(self.file.encode('utf-8')).hexdigest()
	
	def __str__(self):
		return "{} ({}X{}) - {}".format(
			self.file, 
			self.resolution_x, 
			self.resolution_y, 
			self.fingerprint)
		