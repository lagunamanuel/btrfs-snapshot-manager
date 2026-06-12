# Btrfs Snapshot Manager

A GTK4 desktop application to manage Btrfs snapshots visually on Linux.
Built with Python and libadwaita for native GNOME integration.

![Main list](screenshots/list.png)

## 🚀 Features

- **List subvolumes and snapshots** with icons distinguishing each type
- **Create snapshots** with an editable, auto-generated default name
- **Delete snapshots** with a confirmation dialog
- **Search/filter** subvolumes and snapshots by name
- **Snapshot metadata** — creation date and exclusive disk size
- **Empty and error states** with native GNOME styling

## 📸 Screenshots

| Create snapshot | Delete snapshot | Search |
|---|---|---|
| ![Create](screenshots/create.png) | ![Delete](screenshots/delete.png) | ![Search](screenshots/search.png) |

## 🛠️ Prerequisites

- Linux with a Btrfs root filesystem
- Python 3.10+
- GTK4 and libadwaita
- `sudo` access (snapshot operations require root)

```bash
sudo dnf install python3-gobject gtk4 libadwaita   # Fedora
sudo apt install python3-gi gtk4 libadwaita-1-dev  # Ubuntu
```

Enable Btrfs quotas for size reporting:

```bash
sudo btrfs quota enable /
```

## ⚙️ Installation

```bash
git clone https://github.com/lagunamanuel/btrfs-snapshot-manager
cd btrfs-snapshot-manager
python3 main.py
```

## ⚠️ Compatibility Note

This app is designed for Btrfs systems **without a pre-existing snapshot
manager** (e.g. a default Fedora installation). On systems using Snapper
(such as openSUSE or Arch-based distros like Omarchy), snapshots follow a
different structure (`.snapshots/<id>/snapshot` with XML metadata managed
by Snapper). Using this app alongside Snapper is **not recommended**, as
it may interfere with Snapper's own tracking.

## 🗺️ Roadmap

- Snapper-compatible snapshot structure support
- Flatpak / RPM packaging

## 📄 License

This project is licensed under the GPL-3.0 License — see the [LICENSE](LICENSE) file for details.
