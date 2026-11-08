#!/usr/bin/env python3
"""
Compact Spotify TUI banner for fish terminals on CachyOS.
Controls local Spotify via MPRIS and searches via Spotify Web API.

Usage (add to fish config):
  set -g SPOTIFY_CLIENT_ID your_id
  set -g SPOTIFY_CLIENT_SECRET your_secret
  spotify-banner

Controls:
  Space  - Play/Pause
  →      - Next track
  ←      - Previous track
  ←←     - Previous (hold)
  →→     - Seek forward 30s
  ←←     - Seek back 10s
  v      - Volume +/-
  /      - Toggle MPRIS/Web mode
  q      - Quit
"""

import sys
import json
import base64
import urllib.request
import urllib.parse
import time
import os
import select
import tty
import termios

try:
    import dbus
    HAS_DBUS = True
except ImportError:
    HAS_DBUS = False

MPRIS_DBUS_NAME = 'org.mpris.MediaPlayer2.spotify'
MPRIS_OBJECT_PATH = '/org/mpris/MediaPlayer2'
MPRIS_INTERFACE = 'org.mpris.MediaPlayer2.Player'
MPRIS_METADATA_INTERFACE = 'org.freedesktop.DBus.Properties'

CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID', '')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET', '')

token_cache = None


def get_spotify_token():
    global token_cache
    if token_cache and token_cache.get('expires_at', 0) > time.time():
        return token_cache['access_token']

    if not CLIENT_ID or not CLIENT_SECRET:
        return None

    try:
        credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
        encoded = base64.b64encode(credentials.encode()).decode()

        data = urllib.parse.urlencode({
            'grant_type': 'client_credentials',
            'scope': 'user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private'
        }).encode()

        req = urllib.request.Request(
            'https://accounts.spotify.com/api/token',
            data=data,
            method='POST',
            headers={'Authorization': f'Basic {encoded}', 'Content-Type': 'application/x-www-form-urlencoded'}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read().decode())
            result['expires_at'] = time.time() + result['expires_in'] - 30
            token_cache = result
            return result['access_token']
    except Exception:
        return None


def spotify_api_get(path, access_token=None):
    try:
        headers = {'Authorization': f'Bearer {access_token}'} if access_token else {}
        req = urllib.request.Request(f'https://api.spotify.com/v1{path}', headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def get_mpris_metadata():
    if not HAS_DBUS:
        return None
    try:
        bus = dbus.SessionBus()
        proxy = bus.get_object(MPRIS_DBUS_NAME, MPRIS_OBJECT_PATH)
        props = dbus.Interface(proxy, MPRIS_METADATA_INTERFACE)
        metadata = props.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
        position = props.Get('org.mpris.MediaPlayer2.Player', 'Position')
        return {
            'title': metadata.get('xesam:title', 'Unknown'),
            'artist': ', '.join(metadata.get('xesam:artist', ['Unknown'])),
            'album': metadata.get('xesam:album', 'Unknown'),
            'duration_ms': metadata.get('xesam:duration', 0),
            'position_ms': position // 1000,
            'playback': props.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus').lower() == 'playing'
        }
    except Exception:
        return None


def mpris_control(action):
    if not HAS_DBUS:
        return False
    try:
        bus = dbus.SessionBus()
        proxy = bus.get_object(MPRIS_DBUS_NAME, MPRIS_OBJECT_PATH)
        player = dbus.Interface(proxy, MPRIS_INTERFACE)
        actions = {
            'play_pause': player.PlayPause,
            'next': player.Next,
            'previous': player.Previous,
            'play': player.Play,
            'pause': player.Pause,
            'stop': player.Stop
        }
        if action in actions:
            actions[action]()
            return True
        elif action == 'seek':
            player.Seek(30 * 1000000)
            return True
    except Exception:
        pass
    return False


def set_volume(v):
    if not HAS_DBUS:
        return False
    try:
        bus = dbus.SessionBus()
        proxy = bus.get_object(MPRIS_DBUS_NAME, MPRIS_OBJECT_PATH)
        props = dbus.Interface(proxy, MPRIS_METADATA_INTERFACE)
        props.Set('org.mpris.MediaPlayer2.Player', 'Volume', v)
        return True
    except Exception:
        pass
    return False


def get_spotify_playback():
    token = get_spotify_token()
    if not token:
        return None
    data = spotify_api_get('/me/player', token)
    if not data:
        return None

    item = data.get('item', {})
    if not item:
        return None

    return {
        'title': item.get('name', 'Unknown'),
        'artist': ', '.join(a.get('name', '') for a in item.get('artists', [])),
        'album': item.get('album', {}).get('name', 'Unknown'),
        'duration_ms': item.get('duration_ms', 0),
        'position_ms': data.get('progress_ms', 0),
        'playback': data.get('is_playing', False)
    }


def truncate(s, max_len):
    if len(s) <= max_len:
        return s
    return s[:max_len-2] + '…'


def draw_banner(current, width=64):
    lines = []

    status = current.get('playback', False)

    if status:
        play_icon = '⏸'
    else:
        play_icon = '▶'

    title = truncate(current.get('title', 'Unknown'), width-20)
    artist = truncate(current.get('artist', 'Unknown'), width-20)

    pos = current.get('position_ms', 0)
    dur = current.get('duration_ms', 1)
    progress = pos / dur if dur > 0 else 0

    bar_width = width - 22
    filled = int(bar_width * progress)
    bar = '█' * filled + '░' * (bar_width - filled)

    pos_str = f"{pos//1000}:{pos%1000//10:02d}"
    dur_str = f"{dur//1000}:{dur%1000//10:02d}"

    lines.append(f"┌─{'─'*width}┐")
    lines.append(f"│ {play_icon} {title:<{width-4}} │")
    lines.append(f"│ {artist:<{width}} │")
    lines.append(f"│ [{bar}] {pos_str}/{dur_str} │")
    lines.append(f"└─{'─'*width}┘")

    return '\n'.join(lines)


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def kbhit():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


def hide_cursor():
    print('\033[?25l', end='', flush=True)


def show_cursor():
    print('\033[?25h', end='', flush=True)


def clear_lines(n):
    for _ in range(n):
        print('\x1b[A\x1b[K')


def main():
    global CLIENT_ID, CLIENT_SECRET

    if not HAS_DBUS:
        print("MPRIS (local Spotify control) requires python-dbus", file=sys.stderr)

    use_mpris = True
    running = True

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        hide_cursor()

        height = 5
        while running:
            if use_mpris:
                current = get_mpris_metadata()
            else:
                current = get_spotify_playback()

            clear_lines(height)

            if current:
                banner = draw_banner(current)
                print(banner)
            else:
                print("┌─" + "─"*64 + "┐")
                print("│ " + " "*(64) + "│")
                print("│ " + " " * 62 + " │")
                print("│ " + " "*(64) + "│")
                print("│ No Spotify playback | Space=Play/Pause | ←→=Skip | v=Vol | /=Web | q=Quit │")
                print("└─" + "─"*64 + "┘")

            sys.stdout.flush()
            time.sleep(0.5)

            while kbhit():
                ch = sys.stdin.read(1)
                if ch == 'q':
                    running = False
                elif ch == ' ':
                    mpris_control('play_pause')
                elif ch == '\x1b':
                    seq = ch
                    ch2 = sys.stdin.read(1)
                    if ch2 == '[':
                        ch3 = sys.stdin.read(1)
                        if ch3 == 'C':
                            mpris_control('next')
                        elif ch3 == 'D':
                            mpris_control('previous')
                elif ch == 'v':
                    current_vol = 0.5
                    if HAS_DBUS:
                        try:
                            bus = dbus.SessionBus()
                            proxy = bus.get_object(MPRIS_DBUS_NAME, MPRIS_OBJECT_PATH)
                            props = dbus.Interface(proxy, MPRIS_METADATA_INTERFACE)
                            current_vol = props.Get('org.mpris.MediaPlayer2.Player', 'Volume')
                        except:
                            pass
                    new_vol = max(0, min(1, current_vol + 0.1))
                    set_volume(new_vol)
                elif ch == 'z':
                    new_vol = max(0, min(1, current_vol - 0.1))
                    set_volume(new_vol)
                elif ch == '/':
                    use_mpris = not use_mpris
                elif ch == 'h':
                    current = None

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        show_cursor()
        print()


if __name__ == '__main__':
    main()