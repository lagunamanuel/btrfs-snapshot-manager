import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw
import btrfs

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title('Btrfs Snapshot Manager')
        self.set_default_size(800, 500)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(box)

        header = Adw.HeaderBar()
        box.append(header)

        # Scrollable list
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        box.append(scroll)

        self._list = Gtk.ListBox()
        self._list.set_selection_mode(Gtk.SelectionMode.NONE)
        self._list.add_css_class('boxed-list')
        self._list.set_margin_top(12)
        self._list.set_margin_bottom(12)
        self._list.set_margin_start(12)
        self._list.set_margin_end(12)
        scroll.set_child(self._list)

        self._load_subvolumes()

    def _load_subvolumes(self):
        for row in self._list:
            self._list.remove(row)

        subvolumes = btrfs.list_subvolumes()

        for sv in subvolumes:
            row = Adw.ActionRow()
            row.set_title(sv['path'])
            row.set_subtitle(f"ID: {sv['id']}  •  Gen: {sv['gen']}")
            self._list.append(row)