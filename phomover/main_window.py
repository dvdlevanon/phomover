import multiprocessing
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from phomover.screen_utils import *
from phomover.indexer import Indexer
from phomover.fingerprinter import Fingerprinter
from phomover.welcome_screen import WelcomeScreen
from phomover.directories_screen import DirectoriesScreen
from phomover.db_screen import DbScreen
from phomover.resources_screen import ResourcesScreen
from phomover.scan_screen import ScanScreen
from phomover.fingerprint_screen import FingerprintScreen

class MainWindow(Gtk.Window):
	def __init__(self):
		super(Gtk.Window, self).__init__()
		
		self.set_position(Gtk.WindowPosition.CENTER)
		self.connect("key-press-event", self.on_key_press_event)
		self.connect("destroy", self.stop)
		self.set_title("Phomover")
		
		self.cpu_cores = multiprocessing.cpu_count() / 2
		self.indexer = Indexer()
		self.fingerprinter = Fingerprinter()
		
		self.indexer.directories = ["/home/david/pictures"]
		self.indexer.db_file = "/home/david/pictures/phomover.db"
		
		self.welcome_screen = WelcomeScreen(self.welcome_photos_handler, self.welcome_db_handler)
		self.directories_screen = DirectoriesScreen(self.indexer.directories, self.directories_done_handler)
		self.db_screen = DbScreen(self.indexer.db_file, self.db_done_handler)
		self.resources_screen = ResourcesScreen(self.cpu_cores, self.resources_done_handler)
		self.scan_screen = ScanScreen(self.scan_done_handler)
		self.fingerprint_screen = FingerprintScreen(self.fingerprint_done_handler)
		
		self.current_screen = None
		self.replace_current_screen(self.welcome_screen)
		
		# self.indexer.make_sure_database_initialized()
		# self.show_fingerprint_screen()
	
	def welcome_photos_handler(self):
		self.replace_current_screen(self.directories_screen)
	
	def welcome_db_handler(self):
		print("welcome_db_handler")
	
	def directories_done_handler(self, selected_paths):
		self.indexer.directories = selected_paths
		self.replace_current_screen(self.db_screen)
	
	def db_done_handler(self, db_file):
		self.indexer.db_file = db_file
		self.replace_current_screen(self.resources_screen)
	
	def resources_done_handler(self, cpu_cores):
		self.cpu_cores = cpu_cores
		
		if self.indexer.already_indexed():
			show_question_dialog(
				"It seems like the selected database already built, would you like to force re-scanning of all the directories?",
				self.show_scan_screen,
				self.show_fingerprint_screen)
		else:
			self.show_scan_screen()
	
	def scan_done_handler(self):
		self.show_fingerprint_screen()
	
	def show_scan_screen(self):
		self.replace_current_screen(self.scan_screen)
		self.indexer.async_scan(self.scan_screen)
		self.set_size_request(800, 600)
	
	def show_fingerprint_screen(self):
		self.replace_current_screen(self.fingerprint_screen)
		self.fingerprinter.async_fingerprint(self.cpu_cores, self.fingerprint_screen, self.indexer.database)
	
	def fingerprint_done_handler(self):
		print("fingerprint done")
		pass
	
	def reset_screen_size(self):
		self.set_size_request(500, 600)
		self.set_default_size(500, 600)
		
	def replace_current_screen(self, new_screen):
		if self.current_screen != None:
			self.remove(self.current_screen)
		
		self.add(new_screen)
		self.current_screen = new_screen
		self.reset_screen_size()
		self.show_all()
	
	def stop(self, event):
		self.indexer.stop()
		self.fingerprinter.stop()
		Gtk.main_quit()
		 
	def on_key_press_event(self, widget, event):
		if event.keyval == Gdk.KEY_Escape:
			self.stop(event)
