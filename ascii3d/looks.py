"""Look styles with ANSI color support"""

LOOKS = {
    'neo': {
        'name': 'Neo',
        'description': 'Neo style - green/cyan',
        'fg': '\033[38;5;46m',  # Bright green
        'bg': '\033[48;5;235m',
        'reset': '\033[0m'
    },
    'solaris': {
        'name': 'Solaris',
        'description': 'Solaris style - orange',
        'fg': '\033[38;5;208m',  # Orange
        'bg': '\033[48;5;235m',
        'reset': '\033[0m'
    },
    'blueprint': {
        'name': 'Blueprint',
        'description': 'Blueprint style - cyan/white',
        'fg': '\033[38;5;51m',  # Cyan
        'bg': '\033[48;5;235m',
        'reset': '\033[0m'
    },
    'mono': {
        'name': 'Mono',
        'description': 'Monochrome - white',
        'fg': '\033[38;5;15m',  # White
        'bg': '\033[48;5;235m',
        'reset': '\033[0m'
    },
    'signal': {
        'name': 'Signal',
        'description': 'Signal style - green matrix',
        'fg': '\033[38;5;40m',  # Green
        'bg': '\033[48;5;235m',
        'reset': '\033[0m'
    },
    'ember': {
        'name': 'Ember',
        'description': 'Ember style - red/orange',
        'fg': '\033[38;5;202m',  # Orange-red
        'bg': '\033[48;5;235m',
        'reset': '\033[0m'
    },
    'inferno': {
        'name': 'Inferno',
        'description': 'Inferno style - red',
        'fg': '\033[38;5;196m',  # Red
        'bg': '\033[48;5;235m',
        'reset': '\033[0m'
    },
    'drift': {
        'name': 'Drift',
        'description': 'Drift style - blue',
        'fg': '\033[38;5;39m',  # Blue
        'bg': '\033[48;5;235m',
        'reset': '\033[0m'
    },
    'aurora': {
        'name': 'Aurora',
        'description': 'Aurora style - cyan/magenta',
        'fg': '\033[38;5;87m',  # Magenta
        'bg': '\033[48;5;235m',
        'reset': '\033[0m'
    },
    'voltage': {
        'name': 'Voltage',
        'description': 'Voltage style - purple',
        'fg': '\033[38;5;129m',  # Purple
        'bg': '\033[48;5;235m',
        'reset': '\033[0m'
    },
    'noir': {
        'name': 'Noir',
        'description': 'Noir style - gray',
        'fg': '\033[38;5;244m',  # Gray
        'bg': '\033[48;5;235m',
        'reset': '\033[0m'
    }
}

def get_look(name: str):
    """Get look style by name"""
    return LOOKS.get(name.lower(), LOOKS['mono'])

def list_looks():
    """Return list of available looks"""
    return list(LOOKS.keys())
