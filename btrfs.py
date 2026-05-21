# Btrfs operations — isolated from UI
import subprocess
from datetime import datetime

MOUNT_POINT = '/mnt'

def _get_device():
    """Returns the block device of the Btrfs filesystem."""
    result = subprocess.run(
        ['findmnt', '-n', '-o', 'SOURCE', '/'],
        capture_output=True,
        text=True
    )
    source = result.stdout.strip()
    return source.split('[')[0]

def list_subvolumes():
    """Returns a list of Btrfs subvolumes, or None on error."""
    try:
        result = subprocess.run(
            ['sudo', 'btrfs', 'subvolume', 'list', '/'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return None

        subvolumes = []
        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 9:
                subvolumes.append({
                    'id': parts[1],
                    'gen': parts[3],
                    'top_level': parts[6],
                    'path': parts[8]
                })
        return subvolumes
    except Exception:
        return None

def is_snapshot(subvolume):
    """Returns True if the subvolume is a snapshot (lives inside .snapshots)."""
    return subvolume['path'].startswith('.snapshots/')

def default_snapshot_name(subvolume_path):
    """Returns a default snapshot name based on subvolume and current datetime."""
    date = datetime.now().strftime('%Y-%m-%d_%H-%M')
    subvol = subvolume_path.replace('/', '-')
    return f'{subvol}-{date}'

def create_snapshot(subvolume_path, name):
    """Creates a read-only snapshot of a subvolume into .snapshots/name."""
    device = _get_device()
    try:
        subprocess.run(
            ['sudo', 'mount', '-o', 'subvolid=5,rw', device, MOUNT_POINT],
            check=True
        )
        source = f'{MOUNT_POINT}/{subvolume_path}'
        dest = f'{MOUNT_POINT}/.snapshots/{name}'
        result = subprocess.run(
            ['sudo', 'btrfs', 'subvolume', 'snapshot', '-r', source, dest],
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stderr.strip()
    finally:
        subprocess.run(['sudo', 'umount', MOUNT_POINT])

def delete_snapshot(path):
    """Deletes a snapshot from .snapshots."""
    device = _get_device()
    try:
        subprocess.run(
            ['sudo', 'mount', '-o', 'subvolid=5,rw', device, MOUNT_POINT],
            check=True
        )
        target = f'{MOUNT_POINT}/.snapshots/{path.split("/")[-1]}'
        result = subprocess.run(
            ['sudo', 'btrfs', 'subvolume', 'delete', target],
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stderr.strip()
    finally:
        subprocess.run(['sudo', 'umount', MOUNT_POINT])

def is_container(subvolume):
    """Returns True if the subvolume is the .snapshots container itself."""
    return subvolume['path'] == '.snapshots'
