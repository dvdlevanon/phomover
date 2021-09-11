import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

BORDER_MARGINS = 15
DEFAULT_SPACING = 3

def create_markup_label(markup_text):
	label = Gtk.Label()
	label.set_markup(markup_text)
	label.set_line_wrap(True)
	return label

def create_button(label_text, handler):
	label = Gtk.Label(label=label_text)
	button = Gtk.Button()
	label.set_justify(Gtk.Justification.CENTER)
	button.add(label)
	button.connect("clicked", handler)
	return button

def set_margins(widget, margins):
	widget.set_margin_start(margins)
	widget.set_margin_end(margins)
	widget.set_margin_top(margins)
	widget.set_margin_bottom(margins)

def show_error_dialog(text):
	dialog = Gtk.MessageDialog(
		flags=0,
		message_type=Gtk.MessageType.ERROR,
		buttons=Gtk.ButtonsType.CANCEL,
		text=text,
	)
	
	dialog.run()
	dialog.destroy()

def show_question_dialog(question, yes_handler, no_handler):
	dialog = Gtk.MessageDialog(
		flags=0,
		message_type=Gtk.MessageType.QUESTION,
		buttons=Gtk.ButtonsType.YES_NO,
		text=question,
	)
	
	response = dialog.run()
	
	if response == Gtk.ResponseType.YES:
		yes_handler()
	elif response == Gtk.ResponseType.NO:
		no_handler()

	dialog.destroy()
