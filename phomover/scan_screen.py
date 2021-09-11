import os
import time
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Pango
from phomover.screen_utils import *
from phomover.constants import *
from phomover.file_choose_component import FileChooserComponent

header_markup = """
<span font_size="xx-large">Photos Scanning</span>
"""

class ScanScreen(Gtk.VBox):
	def __init__(self, done_handler):
		Gtk.VBox.__init__(self)
		
		self.found_dirs = {}
		self.scanned_directories = 0
		self.scanned_photos = 0
		
		header_label = create_markup_label(header_markup)
		self.spinner = Gtk.Spinner()
		status_frame = self.build_status_frame()
		detailed_status = self.build_detailed_status()
		
		self.done_button = create_button("Done", self.done_clicked)
		self.done_button.set_sensitive(False)
		
		self.pack_start(header_label, False, False, DEFAULT_SPACING)
		self.pack_start(self.spinner, False, False, DEFAULT_SPACING)
		self.pack_start(status_frame, False, False, DEFAULT_SPACING)
		self.pack_start(detailed_status, True, True, DEFAULT_SPACING)
		self.pack_start(self.done_button, False, False, DEFAULT_SPACING)
		
		set_margins(self, BORDER_MARGINS)
		
		self.done_handler = done_handler
	
	def build_status_frame(self):
		self.status_files_label = StatusLabel("images/image.png", "0 Photos Found")
		self.status_directories_label = StatusLabel("images/folder.png", "0 Directories Scanned")
		self.current_directory_label = Gtk.Label("Current directory: ")
		self.current_directory_label.set_ellipsize(Pango.EllipsizeMode.END)
		
		counters_hbox = Gtk.HBox()
		counters_hbox.pack_start(self.status_files_label, True, False, DEFAULT_SPACING)
		counters_hbox.pack_end(self.status_directories_label, True, False, DEFAULT_SPACING)
		
		dir_hbox = Gtk.HBox()
		dir_hbox.pack_start(self.current_directory_label, False, False, DEFAULT_SPACING)
		
		vbox = Gtk.VBox()
		vbox.pack_start(counters_hbox, False, False, DEFAULT_SPACING * 4)
		vbox.pack_start(dir_hbox, False, False, DEFAULT_SPACING)
		set_margins(vbox, BORDER_MARGINS / 2)
		
		frame = Gtk.Frame()
		frame.add(vbox)
		return frame
	
	def build_detailed_status(self):
		self.details_listbox = Gtk.ListBox()
		self.details_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		self.details_scroll = Gtk.ScrolledWindow()
		self.details_scroll.add(self.details_listbox)
		
		frame = Gtk.Frame()
		frame.add(self.details_scroll)
		
		return frame 
	
	def done_clicked(self, event):
		self.done_handler()
	
	def update_current_directory(self, directory):
		self.status_directories_label.update_text(str(self.scanned_directories) + " Directories Scanned")
		self.current_directory_label.set_label("Current directory: " + directory)
		
	def update_found_photo(self, photo):
		self.status_files_label.update_text(str(self.scanned_photos) + " Photos Found")
		
		directory = os.path.dirname(photo)
		if not directory in self.found_dirs:
			item = ListItem(directory)
			self.found_dirs[directory] = {
				'count': 0,
				'item': item
			}
			self.details_listbox.add(item)
			self.show_all()
			self.details_scroll.get_vadjustment().set_value(self.details_scroll.get_vadjustment().get_upper())
		
		found_dir = self.found_dirs[directory]
		found_dir['count'] = found_dir['count'] + 1
		found_dir['item'].update_count(found_dir['count'])
	
	def update_completion(self):
		self.spinner.stop()
		self.done_button.set_sensitive(True)
		self.current_directory_label.set_label("Completed")
	
	def scan_start(self):
		self.spinner.start()
	
	def scanning_directory(self, directory):
		self.scanned_directories = self.scanned_directories + 1
		GLib.idle_add(self.update_current_directory, directory)
		
	def scanning_photo(self, photo):
		self.scanned_photos = self.scanned_photos + 1
		time.sleep(SLEEP_COOLDOWN_MILLIS)
		GLib.idle_add(self.update_found_photo, photo)
		
	def scanning_other_file(self, file):
		pass
	
	def scan_complete(self):
		GLib.idle_add(self.update_completion)

class StatusLabel(Gtk.HBox):
	def __init__(self, image_path, initial_text):
		Gtk.HBox.__init__(self)
		
		self.label = Gtk.Label()
		self.label.set_markup(self.build_markup(initial_text))
		image = Gtk.Image.new_from_file(image_path)
		
		self.pack_start(image, False, False, DEFAULT_SPACING)
		self.pack_start(self.label, False, False, DEFAULT_SPACING)
	
	def build_markup(self, text):
		return """<span font_size="large">""" + text + "</span>"
	
	def update_text(self, text):
		self.label.set_markup(self.build_markup(text))

class ListItem(Gtk.ListBoxRow):
	def __init__(self, directory):
		Gtk.ListBoxRow.__init__(self)
		
		directory_label = Gtk.Label(label=directory)
		self.count_label = Gtk.Label()
		
		directory_label.set_ellipsize(Pango.EllipsizeMode.START)
		directory_label.set_selectable(True)
		
		hbox = Gtk.HBox()
		hbox.pack_start(directory_label, False, False, DEFAULT_SPACING * 5)
		hbox.pack_end(self.count_label, False, False, DEFAULT_SPACING)
		self.add(hbox)
	
	def update_count(self, count):
		self.count_label.set_label(str(count))
		