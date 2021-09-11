import multiprocessing
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from phomover.screen_utils import *

header_markup = """
<span font_size="xx-large">System Resources.</span>
"""

content_markup = """
<big>Choose how many system resources will be used during the Database building.</big>

As the building process may take long, depending on the amount of photos you have, we prefer to run it in parallel using multiple CPU cores. However we don't want to use all the system resources, you should be able to continue using the machine during the process.

If you plan to run it at night, or when you are away, please give it the maximum CPU cores for faster processing.

Leave default selection in case of doubt.
"""

class ResourcesScreen(Gtk.VBox):
	def __init__(self, initial_cpu_count, done_handler):
		Gtk.VBox.__init__(self)
		
		header_label = create_markup_label(header_markup)
		content_label = create_markup_label(content_markup)
		self.cpu_scale = Gtk.HScale()
		done_button = Gtk.Button(label="Done")
		done_button.connect("clicked", self.done_clicked)
		
		self.cpu_scale.set_range(1, multiprocessing.cpu_count())
		self.cpu_scale.set_value(initial_cpu_count)
		self.cpu_scale.set_digits(False)
		
		hbox = Gtk.HBox()
		minLabel = Gtk.Label(label="1")
		maxLabel = Gtk.Label(label=str(multiprocessing.cpu_count()))
		
		hbox.pack_start(minLabel, False, False, DEFAULT_SPACING)
		hbox.pack_start(self.cpu_scale, True, True, DEFAULT_SPACING)
		hbox.pack_start(maxLabel, False, False, DEFAULT_SPACING)
		
		set_margins(self, BORDER_MARGINS)
		
		self.pack_start(header_label, False, False, DEFAULT_SPACING)
		self.pack_start(content_label, False, False, DEFAULT_SPACING)
		self.pack_start(hbox, False, False, DEFAULT_SPACING)
		self.pack_end(done_button, False, False, DEFAULT_SPACING)
		
		self.done_handler = done_handler
	
	def done_clicked(self, event):
		self.done_handler(self.cpu_scale.get_value())
