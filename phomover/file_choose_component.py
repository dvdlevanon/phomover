import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class FileChooserComponent(Gtk.HBox):
	def __init__(self, should_create_x_button, x_handler, dialog_action, dialog_title):
		Gtk.HBox.__init__(self)
		
		self.set_spacing(5)
		
		self.path = Gtk.Entry()
		self.path.set_placeholder_text("Enter manually or choose by clicking ...")
		
		self.button = Gtk.Button(label="...")
		self.button.connect("clicked", self.choose_directory_clicked)
		
		if should_create_x_button:
			x_button = Gtk.Button(label="X")
			x_button.connect("clicked", self.x_clicked)
			self.pack_start(x_button, False, False, 0)
		
		self.pack_start(self.path, True, True, 0)
		self.pack_start(self.button, False, False, 0)
		
		self.button.grab_focus()
		self.x_handler = x_handler
		self.dialog_title = dialog_title
		self.dialog_action = dialog_action
	
	def choose_directory_clicked(self, event):
		dialog = Gtk.FileChooserDialog(
			title=self.dialog_title,
			action=self.dialog_action,
		)
		
		if (self.dialog_action != Gtk.FileChooserAction.SELECT_FOLDER):
			filter_any = Gtk.FileFilter()
			filter_any.set_name("Any files")
			filter_any.add_pattern("*")
			dialog.add_filter(filter_any)
		
		dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK)
		dialog.set_default_size(600, 400)

		response = dialog.run()
		
		if response == Gtk.ResponseType.OK:
			self.path.set_text(dialog.get_filename())

		dialog.destroy()

	def x_clicked(self, event):
		self.x_handler(self)
	
	def get_selected_file(self):
		return self.path.get_text()
	
	def set_selected_file(self, file):
		self.path.set_text(file)
