import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw
from window import MainWindow

class Application(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.github.lagunamanuel.btrfs-snapshot-manager')
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        win = MainWindow(application=app)
        win.present()

def main():
    app = Application()
    app.run()

if __name__ == '__main__':
    main()
