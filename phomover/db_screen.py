import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from phomover.screen_utils import *
from phomover.file_choose_component import FileChooserComponent

header_markup = """
<span font_size="xx-large">Choose Database location.</span>
"""

content_markup = """
<big>Please choose a location where the Database will be stored.</big>

Its better to choose a fast location (SSD) as we'll use it intensively during the indexing and validation phases.

You may choose an existing Database in order to update it, or a new one if this is the initial time. Name the Database file whatever you like including the extension, the only important thing is to remember it.
"""

class DbScreen(Gtk.VBox):
	def __init__(self, initial_db_file, done_handler):
		Gtk.VBox.__init__(self)
		
		header_label = create_markup_label(header_markup)
		content_label = create_markup_label(content_markup)
		self.db_chooser = FileChooserComponent(False, None, Gtk.FileChooserAction.SAVE, "Choose or create a Database")
		
		if initial_db_file != None:
			self.db_chooser.set_selected_file(initial_db_file)
		
		done_button = Gtk.Button(label="Done")
		done_button.connect("clicked", self.done_clicked)
		
		set_margins(self, BORDER_MARGINS)
		
		self.pack_start(header_label, False, False, DEFAULT_SPACING)
		self.pack_start(content_label, False, False, DEFAULT_SPACING)
		self.pack_start(self.db_chooser, False, False, DEFAULT_SPACING)
		self.pack_end(done_button, False, False, DEFAULT_SPACING)
		
		self.done_handler = done_handler
	
	def done_clicked(self, event):
		if self.db_chooser.get_selected_file() == "":
			show_error_dialog("No Database selected")
			return False
		
		self.done_handler(self.db_chooser.get_selected_file())