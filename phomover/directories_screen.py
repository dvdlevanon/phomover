import os
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from phomover.screen_utils import *
from phomover.file_choose_component import FileChooserComponent

header_markup = """
<span font_size="xx-large">Choose photos.</span>
"""

content_markup = """
<big>Please choose one or more directories that contain your photos.</big>

For better performance, please try to be as specific as you can. Choosing a huge directory (e.g. home folder) containing your photos along with lots of other files is not recomended. Try to choose the parent directory containing your photos.
"""

class DirectoriesScreen(Gtk.VBox):
	def __init__(self, initial_directories, done_handler):
		Gtk.VBox.__init__(self)
		
		header_label = create_markup_label(header_markup)
		content_label = create_markup_label(content_markup)
		self.choosers = Gtk.VBox()
		add_directory_button = Gtk.Button(label="Add directory")
		done_button = Gtk.Button(label="Done")
		
		add_directory_button.connect("clicked", self.add_directory_clicked)
		done_button.connect("clicked", self.done_clicked)
		
		self.directoryChoosers = []
		
		if len(initial_directories) > 0:
			first = True
			for directory in initial_directories:
				self.directoryChoosers.append(self.create_file_chooser(not first, directory))
				first = False
		else:
			self.directoryChoosers.append(self.create_file_chooser(False, ""))
		
		self.choosers.pack_start(self.directoryChoosers[0], False, False, DEFAULT_SPACING)
		self.choosers.pack_end(add_directory_button, False, False, DEFAULT_SPACING)
		
		set_margins(self, BORDER_MARGINS)
		
		self.pack_start(header_label, False, False, DEFAULT_SPACING)
		self.pack_start(content_label, False, False, DEFAULT_SPACING)
		self.pack_start(self.choosers, False, False, DEFAULT_SPACING)
		self.pack_end(done_button, False, False, DEFAULT_SPACING)
		
		self.done_handler = done_handler
		
	def add_directory_clicked(self, event):
		newChooser = self.create_file_chooser(True, "")
		self.choosers.pack_start(newChooser, False, False, DEFAULT_SPACING)
		self.directoryChoosers.append(newChooser)
		self.show_all()
	
	def create_file_chooser(self, should_create_x_button, initial_directory):
		result = FileChooserComponent(
			should_create_x_button, 
			self.remove_directory_clicked, 
			Gtk.FileChooserAction.SELECT_FOLDER,
			"Choose a directory with photos")
		
		if initial_directory != "":
			result.set_selected_file(initial_directory)
		
		return result
	
	def remove_directory_clicked(self, chooser):
		self.directoryChoosers.remove(chooser)
		self.choosers.remove(chooser)
	
	def done_clicked(self, event):
		invalid_paths = []
		selected_paths = []
		for current in self.directoryChoosers:
			if current.get_selected_file() == "":
				continue
			elif not os.path.isdir(current.get_selected_file()):
				invalid_paths.append(current.get_selected_file())
			else:
				selected_paths.append(current.get_selected_file())
		
		if len(invalid_paths) > 0:
			show_error_dialog("Those directories are missing:\n\t> " + "\n\t> ".join(invalid_paths))
			return False
		
		if len(selected_paths) == 0:
			show_error_dialog("No directories selected")
			return False
		
		self.done_handler(selected_paths)
	