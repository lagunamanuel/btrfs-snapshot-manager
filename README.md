# btrfs-snapshot-manager
A GTK4 desktop app to manage Btrfs snapshots visually
Built with Python and libadwaita for native GNOME integration.

## 🚀 Features (planned)

- List existing Btrfs snapshots
- Create new snapshots
- Delete snapshots with confirmation dialog
- Native GNOME UI with libadwaita

## 🛠️ Prerequisites

- Linux with a Btrfs filesystem
- Python 3.10+
- GTK4 and libadwaita

```bash
sudo dnf install python3-gobject gtk4 libadwaita   # Fedora
sudo apt install python3-gi gtk4 libadwaita-1-dev  # Ubuntu
```

## ⚙️ Installation

```bash
git clone https://github.com/lagunamanuel/btrfs-snapshot-manager
cd btrfs-snapshot-manager
python3 main.py
```

## 📄 License

This project is licensed under the GPL-3.0 License — see the [LICENSE](LICENSE) file for details.