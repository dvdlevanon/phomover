import os
import time
import threading
import concurrent.futures
import imagehash
from PIL import Image

from phomover.database import Database
from phomover.photo import Photo

class Fingerprinter:
	def __init__(self):
		self.database = None
		self.fingerprint_listener = None
		self.fingerprint_thread = None
		self.should_stop = False
		self.executor = None
		self.processing_inflight = 0
		self.results = {}
	
	def stop(self):
		self.should_stop = True
		
		if self.fingerprint_thread != None:
			print("Waiting for fingerprint threads..")
			self.fingerprint_thread.join()
	
	def async_fingerprint(self, cpu_cores, fingerprint_listener, database):
		if self.fingerprint_thread == None:
			self.fingerprint_thread = threading.Thread(target=self.fingerprint, args=(cpu_cores, fingerprint_listener, database,))
			self.fingerprint_thread.start()
	
	def fingerprint(self, cpu_cores, fingerprint_listener, database):
		self.database = database
		self.fingerprint_listener = fingerprint_listener
		self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=cpu_cores, thread_name_prefix="fingerprint-thread")
		
		photo_paths = self.database.get_photos_without_fingerprint()
		futures = []
		
		for photo_path in photo_paths:
			futures.append(self.executor.submit(self.process_photo, photo_path[0]))
		
		if not self.wait_for_workers(futures):
			return
		
		self.fingerprint_listener.processing_complete()
			
	def wait_for_workers(self, futures):
		total = len(futures)
		
		if total == 0:
			return True
		
		done_count = 0
		
		while True:
			finished_futures = self.get_finished_futures(futures)
			done_count = done_count + len(finished_futures)
			updated_photos = self.get_results(finished_futures)
			
			for finished_future in finished_futures:
				futures.remove(finished_future)
			
			self.fingerprint_listener.progress_updated(done_count, total)
			self.database.update_photos(updated_photos)
			
			if done_count == total:
				break
			
			time.sleep(0.1)
		
		return True
	
	def get_finished_futures(self, futures):
		result = []
		
		for future in futures:
			if self.should_stop:
				return result
				
			if future.done():
				result.append(future)
		
		return result
	
	def get_results(self, futures):
		results = []
		
		for future in futures:
			try:
				results.append(future.result())
			except Exception as e:
				print("Error processing photo " + str(e))
		
		return results
	
	def process_photo(self, photo_path):
		if self.should_stop:
			return
		
		photo = Photo(photo_path)
		loaded_photo = Image.open(photo_path)
		fingerprint = imagehash.average_hash(loaded_photo)
		loaded_photo.close()
		width, height = loaded_photo.size
		
		photo.fingerprint = str(fingerprint)
		photo.resolution_x = width
		photo.resolution_y = height
		
		return photo
