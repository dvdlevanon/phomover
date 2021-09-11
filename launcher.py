import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from phomover.main_window import MainWindow

window = MainWindow()

window.show_all()
Gtk.main()
