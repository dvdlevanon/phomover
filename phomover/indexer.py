import os
import time
import threading

from phomover.constants import *
from phomover.database import Database
from phomover.photo import Photo

class Indexer:
	def __init__(self):
		self.directories = []
		self.db_file = None
		self.scan_thread = None
		self.should_stop = False
		self.database = None
		self.scan_listener = None
	
	def stop(self):
		self.should_stop = True
		
		if self.scan_thread != None:
			print("Waiting for scan thread..")
			self.scan_thread.join()
	
	def make_sure_database_initialized(self):
		if self.database == None:
			self.database = Database(self.db_file)
		
	def already_indexed(self):
		self.make_sure_database_initialized()
		return self.database.get_photos_count() > MINIMUM_FILES_IN_DB
	
	def async_scan(self, scan_listener):
		if self.scan_thread == None:
			self.scan_thread = threading.Thread(target=self.scan, args=(scan_listener,))
			self.scan_thread.start()
	
	def scan(self, scan_listener):
		self.make_sure_database_initialized()
		self.scan_listener = scan_listener
		self.scan_listener.scan_start()
		
		for directory in self.directories:
			self.scan_directory(directory)
		
		self.scan_listener.scan_complete()
		
	def scan_directory(self, directory):
		if self.should_stop:
			return
		
		self.scan_listener.scanning_directory(directory)
		
		for child in os.listdir(directory):
			if self.should_stop:
				return
			
			filename = os.path.join(directory, child)
			if os.path.isdir(filename):
				self.scan_directory(filename)
			elif self.is_photo(filename):
				self.scan_listener.scanning_photo(filename)
				self.add_photo(filename)
			else:
				self.scan_listener.scanning_other_file(filename)

	def is_photo(self, file):
		return (file.endswith(".jpg") or
				file.endswith(".jpeg") or
				file.endswith(".bmp") or
				file.endswith(".png"))
	
	def add_photo(self, photo_file):
		photo = Photo(photo_file)
		self.database.save_new(photo)
