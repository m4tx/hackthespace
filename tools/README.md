# Asset generators

One-off scripts that generate two of the puzzle assets. Their outputs are
committed under `static/`, so you only need these when you want to change a
puzzle or reproduce its asset from scratch.

## Usage

```
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt

# audio spectrum also needs ffmpeg and taglib installed system-wide, e.g.:
#   Debian:     sudo apt install ffmpeg libtag1-dev
#   Arch Linux: sudo pacman -S ffmpeg taglib

cd tools
python generate_audio_spectrum.py   # -> output/deadlyfox.ogg (+ .mp3)
python generate_stego_mix.py        # -> output/lookcloser.jpg
```

Then copy the results over the committed assets:

* `output/deadlyfox.ogg`  -> `static/static/audio/deadlyfox.ogg`
* `output/lookcloser.jpg` -> `static/static/images/generated/lookcloser.jpg`

The next-puzzle URL embedded in each asset is hard-coded near the top of the
respective script; update it if the puzzle order in `src/main.rs` changes.

