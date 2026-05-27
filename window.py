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

        self._del_btn = Gtk.Button(icon_name='user-trash-symbolic')
        self._del_btn.set_tooltip_text('Delete snapshot')
        self._del_btn.set_sensitive(False)
        self._del_btn.add_css_class('destructive-action')
        self._del_btn.connect('clicked', self._on_delete_snapshot)
        header.pack_end(self._del_btn)

        self._add_btn = Gtk.Button(icon_name='list-add-symbolic')
        self._add_btn.set_tooltip_text('Create snapshot')
        self._add_btn.set_sensitive(False)
        self._add_btn.connect('clicked', self._on_create_snapshot)
        header.pack_end(self._add_btn)

        refresh_btn = Gtk.Button(icon_name='view-refresh-symbolic')
        refresh_btn.set_tooltip_text('Refresh')
        refresh_btn.connect('clicked', lambda _: self._load_subvolumes())
        header.pack_end(refresh_btn)

        box.append(header)

        # Stack to switch between list, empty state and error state
        self._stack = Gtk.Stack()
        self._stack.set_vexpand(True)
        box.append(self._stack)

        # --- Normal list view ---
        scroll = Gtk.ScrolledWindow()
        self._list = Gtk.ListBox()
        self._list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self._list.add_css_class('boxed-list')
        self._list.set_margin_top(12)
        self._list.set_margin_bottom(12)
        self._list.set_margin_start(12)
        self._list.set_margin_end(12)
        self._list.connect('row-selected', self._on_row_selected)
        scroll.set_child(self._list)
        self._stack.add_named(scroll, 'list')

        # --- No snapshots yet ---
        empty_page = Adw.StatusPage()
        empty_page.set_icon_name('camera-photo-symbolic')
        empty_page.set_title('No Snapshots Yet')
        empty_page.set_description('No snapshots found. Select a subvolume and press + to create one.')
        self._stack.add_named(empty_page, 'empty')

        # --- Error state ---
        error_page = Adw.StatusPage()
        error_page.set_icon_name('dialog-warning-symbolic')
        error_page.set_title('Could Not Load Subvolumes')
        error_page.set_description('Make sure Btrfs is available and you have the required permissions.')
        self._stack.add_named(error_page, 'error')

        self._selected_subvolume = None
        self._load_subvolumes()

    def _load_subvolumes(self):
        while child := self._list.get_first_child():
            self._list.remove(child)

        self._selected_subvolume = None
        self._add_btn.set_sensitive(False)
        self._del_btn.set_sensitive(False)

        subvolumes = btrfs.list_subvolumes()

        if subvolumes is None:
            self._stack.set_visible_child_name('error')
            return

        if not subvolumes:
            self._stack.set_visible_child_name('empty')
            return

        for sv in subvolumes:
            if btrfs.is_container(sv):
                continue
            row = Adw.ActionRow()
            row.set_title(sv['path'])
            row.set_subtitle(f"ID: {sv['id']}  •  Gen: {sv['gen']}")
            row._subvolume = sv

            if btrfs.is_snapshot(sv):
                icon = Gtk.Image.new_from_icon_name('camera-photo-symbolic')
                icon.add_css_class('dim-label')
                row.add_prefix(icon)
            else:
                icon = Gtk.Image.new_from_icon_name('drive-harddisk-symbolic')
                row.add_prefix(icon)

            self._list.append(row)

        self._stack.set_visible_child_name('list')

    def _on_row_selected(self, listbox, row):
        if row:
            sv = row._subvolume
            self._selected_subvolume = sv
            is_snap = btrfs.is_snapshot(sv)
            self._add_btn.set_sensitive(not is_snap and not btrfs.is_container(sv))
            self._del_btn.set_sensitive(is_snap)
        else:
            self._selected_subvolume = None
            self._add_btn.set_sensitive(False)
            self._del_btn.set_sensitive(False)

    def _on_create_snapshot(self, _):
        sv = self._selected_subvolume
        if not sv:
            return

        default_name = btrfs.default_snapshot_name(sv['path'])

        dialog = Adw.MessageDialog(
            transient_for=self,
            heading='Create Snapshot',
            body=f"Creating snapshot of '{sv['path']}'",
        )

        entry = Gtk.Entry()
        entry.set_text(default_name)
        entry.set_margin_top(8)
        dialog.set_extra_child(entry)

        dialog.add_response('cancel', 'Cancel')
        dialog.add_response('create', 'Create')
        dialog.set_default_response('create')
        dialog.set_response_appearance('create', Adw.ResponseAppearance.SUGGESTED)

        dialog.connect('response', self._on_dialog_response, entry, sv)
        dialog.present()

    def _on_dialog_response(self, dialog, response, entry, sv):
        if response != 'create':
            return

        name = entry.get_text().strip()
        if not name:
            return

        success, error = btrfs.create_snapshot(sv['path'], name)
        if success:
            self._load_subvolumes()
        else:
            self._show_error(error or 'Could not create snapshot.')

    def _on_delete_snapshot(self, _):
        sv = self._selected_subvolume
        if not sv or not btrfs.is_snapshot(sv):
            return

        dialog = Adw.MessageDialog(
            transient_for=self,
            heading='Delete Snapshot',
            body=f"Are you sure you want to delete '{sv['path']}'? This cannot be undone.",
        )

        dialog.add_response('cancel', 'Cancel')
        dialog.add_response('delete', 'Delete')
        dialog.set_default_response('cancel')
        dialog.set_response_appearance('delete', Adw.ResponseAppearance.DESTRUCTIVE)

        dialog.connect('response', self._on_delete_response, sv)
        dialog.present()

    def _on_delete_response(self, dialog, response, sv):
        if response != 'delete':
            return

        success, error = btrfs.delete_snapshot(sv['path'])
        if success:
            self._load_subvolumes()
        else:
            self._show_error(error or 'Could not delete snapshot.')

    def _show_error(self, message):
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading='Error',
            body=message,
        )
        dialog.add_response('ok', 'OK')
        dialog.present()
