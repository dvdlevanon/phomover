import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from phomover.screen_utils import *

header_markup = """
<span font_size="xx-large">Caluclating Photos Fingerprint.</span>
"""

content_markup = """
<big>A photo fingerprint can be used for detecting similar photos.</big>

The process of fingerprint caluclation may take a while, depending on the amount of photos. You may stop and restart the program during the process, it will continue from the position it stopped.

Once the process is done, we'll be able to show you a report with all duplicated/similar photos
"""

class FingerprintScreen(Gtk.VBox):
	def __init__(self, done_handler):
		Gtk.VBox.__init__(self)
		
		header_label = create_markup_label(header_markup)
		content_label = create_markup_label(content_markup)
		
		self.progressbar = Gtk.ProgressBar()
		self.progressbar.set_fraction(0)
		self.progressbar.set_size_request(50, 50)
		self.progress_label = Gtk.Label(label="0/0")
		vbox = Gtk.VBox()
		vbox.pack_start(self.progressbar, False, False, DEFAULT_SPACING)
		vbox.pack_start(self.progress_label, False, False, DEFAULT_SPACING)
		
		set_margins(self, BORDER_MARGINS)
		
		self.pack_start(header_label, False, False, DEFAULT_SPACING)
		self.pack_start(content_label, False, False, DEFAULT_SPACING)
		self.pack_start(vbox, True, False, DEFAULT_SPACING)
		
		self.done_handler = done_handler
	
	def update_progress(self, done_count, total_count):
		self.progress_label.set_label(str(done_count) + "/" + str(total_count))
		self.progressbar.set_fraction(done_count / total_count)
		
	def progress_updated(self, done_count, total_count):
		GLib.idle_add(self.update_progress, done_count, total_count)
	
	def processing_complete(self):
		GLib.idle_add(self.done_handler)
