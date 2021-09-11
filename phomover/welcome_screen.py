import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from phomover.screen_utils import *

header_markup = """
<span font_size="xx-large">Welcome to Phomover.</span>
"""

content_markup = """
<big>This program helps to find, detect and remove duplicate or similar photos from your local storage.</big>

We support photo galleries with 100,000+ photos, residing in various directories, we'll also allow you to verify what is going to be deleted before the actual removal.

For this to work, we first build a Database with all the required information about the photos. Then, we use it in the validation and removal phase. The database building process may take a long time, and consume a lot of system resources (configurable). The two steps allows you to build an Database once, during the night maybe, and use it later for validation and actual removal of the photos.
"""

footer_markup = """
<big>Please choose an option below to continue.</big>
"""

class WelcomeScreen(Gtk.VBox):
	def __init__(self, photos_handler, db_handler):
		Gtk.VBox.__init__(self)
		
		header_label = create_markup_label(header_markup)
		content_label = create_markup_label(content_markup)
		footer_label = create_markup_label(footer_markup)
		
		photos_button = create_button(
			"I want to build or extend a Database\nlet me choose my photos directory",
			self.photos_button_clicked)
		
		db_button = create_button(
			"I already built a Database\nlet me choose my existing Database file", 
			self.db_button_clicked)
		
		self.pack_start(header_label, False, False, DEFAULT_SPACING)
		self.pack_start(content_label, False, False, DEFAULT_SPACING)
		self.pack_start(footer_label, False, False, DEFAULT_SPACING)
		self.pack_end(db_button, False, False, DEFAULT_SPACING)
		self.pack_end(photos_button, False, False, DEFAULT_SPACING)

		set_margins(self, BORDER_MARGINS)
		
		self.photos_handler = photos_handler
		self.db_handler = db_handler
	
	def db_button_clicked(self, button):
		self.db_handler()
		return True
		
	def photos_button_clicked(self, button):
		self.photos_handler()
		return True
