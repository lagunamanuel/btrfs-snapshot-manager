# Btrfs operations — isolated from UI
import subprocess

def list_subvolumes():
    """Returns a list of Btrfs subvolumes on the system."""
    result = subprocess.run(
        ['sudo', 'btrfs', 'subvolume', 'list', '/'],
        capture_output=True,
        text=True
    )

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