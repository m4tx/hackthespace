#!/usr/bin/env python3
"""One-off generator for the "audio spectrum" puzzle asset.

Hides the next-puzzle URL in the audio spectrogram of ``deadlyfox.ogg`` and
mixes it into the source track. Ported out of the old Django management command
``generate_audio_spectrum_assets`` (see git history before commit f4ab363).

This is NOT part of the Rust build -- OGG Vorbis / MP3 encoding and audio
mixing have no practical pure-Rust story, so this stays as a manual Python
tool. Run it when the asset needs regenerating, then copy the resulting
``output/deadlyfox.ogg`` over ``static/static/audio/deadlyfox.ogg``.

Requires: Pillow, pydub (+ ffmpeg), pytaglib (+ taglib). See requirements.txt.

Usage:
    cd tools && python generate_audio_spectrum.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import taglib  # noqa: E402
from PIL import Image  # noqa: E402
from pydub import AudioSegment  # noqa: E402

from common import fill_image_with_rgb_noise, put_text_on_image  # noqa: E402
from vendor.spectrology import convert  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_PATH = os.path.join(HERE, "assets", "deadlyfox.ogg")
OUTPUT_DIR = os.path.join(HERE, "output")

# The URL of the puzzle that follows "audio_spectrum" (keypad) in the Rust
# router (src/main.rs).
NEXT_PUZZLE_URL = "/doorkeypad/"

# Values previously kept in the Django settings (PUZZLE_AUDIO_SPECTRUM_*).
FONT_NAME = "Roboto/Roboto-Black.ttf"
FONT_SIZE = 125
MIN_FREQ = 14000
MAX_FREQ = 17000
PIXELS_PER_SECOND = 30
AUDIO_POSITION = 5000  # milliseconds
AUDIO_GAIN = -35  # dB
TAGS = {
    "ARTIST": ["SFI"],
    "ALBUM": ["Surfing in Space"],
    "TITLE": ["Deadly Fox"],
    "DATE": ["2019"],
    "TRACKNUMBER": ["9/11"],
    "COMMENT": ["000000A5 000000CC 000096C2 00000022 0000C9EE 0000006A"],
}


def gen_image(out_path):
    img = Image.new("RGBA", (800, 200), (0, 0, 0, 0))
    fill_image_with_rgb_noise(img)
    put_text_on_image(img, NEXT_PUZZLE_URL, FONT_NAME, FONT_SIZE, (0, 0, 0, 255))
    img.save(out_path)


def combine_audio(source_path, wav_path):
    sound1 = AudioSegment.from_ogg(source_path)
    sound2 = AudioSegment.from_wav(wav_path).apply_gain(AUDIO_GAIN)
    return sound1.overlay(sound2, position=AUDIO_POSITION)


def set_metadata(file_path):
    song = taglib.File(file_path)
    for key, value in TAGS.items():
        song.tags[key] = value
    song.save()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_base = os.path.join(OUTPUT_DIR, "deadlyfox")

    with tempfile.NamedTemporaryFile(suffix=".png") as img_file, \
            tempfile.NamedTemporaryFile(suffix=".wav") as wav_file:
        print("Generating image")
        gen_image(img_file.name)
        print("Generating audio (this may take a while)")
        convert(img_file.name, wav_file.name, MIN_FREQ, MAX_FREQ,
                PIXELS_PER_SECOND, 44100, False, False)
        print("Mixing audio")
        output = combine_audio(SOURCE_PATH, wav_file.name)
        print("Saving the files")
        output.export(out_base + ".mp3", bitrate="256k", format="mp3")
        output.export(out_base + ".ogg", bitrate="256k", format="ogg")
        print("Saving the metadata")
        set_metadata(out_base + ".mp3")
        set_metadata(out_base + ".ogg")
        print("Done! Output in", OUTPUT_DIR)


if __name__ == "__main__":
    main()
