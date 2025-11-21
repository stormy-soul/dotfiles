import os
import time
import eyed3
import tempfile
import subprocess
from mpd import MPDClient
from pathlib import Path
from typing import Optional, Union

exception_buff = []

def extract(track: Path) -> Optional[Path]:
    audio = eyed3.load(track)
    if not audio or not audio.tag or not audio.tag.images:
        exception_buff.append("track data unavailable")
        return None

    try:
        temp = tempfile.NamedTemporaryFile(
            suffix = ".png",
            delete = False
        )
        temp.write(audio.tag.images[0].image_data)
        temp.close()
        return temp.name
    except Exception as e:
        exception_buff.append(e)
        return None

def notify(icon: Union[str, Path], title: str, body: str) -> None:
    try:
        process = subprocess.Popen(["notify-send", "-i", icon, "-a", "rmpc", "-t", "2500", title, body])
    except Exception as e:
        exception_buff.append(e)
    
if __name__ == "__main__":
    client = MPDClient()
    client.connect("localhost", 6600)
    song = client.currentsong()

    music_path = Path("/home/nadun/Music/")
    track_path = music_path / song['file']
    cover_path = extract(track_path)


    notify(cover_path or "audio-x-generic", f"{song['title']}", f"{'[E] ' + ', '.join(str(exception) for exception in exception_buff) if len(exception_buff) != 0 else song['artist']}")

    if cover_path:
        time.sleep(1)
        try:
            os.remove(cover_path)
        except Exception as e:
            print(f"[E] error while cleaning up: {e}")

