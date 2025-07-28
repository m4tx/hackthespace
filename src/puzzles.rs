use cot::request::extractors::FromRequestHead;
use cot::router::Urls;

const PUZZLE_ORDER: [&str; 13] = [
    "rot13",
    "sky",
    "image",
    "terminal",  // Requires hard-coding the next puzzle
    "redirect",
    "login",
    "pages",
    "audio_spectrum",
    "keypad",
    "vigenere",
    "stego_mix",
    "reverse",
    "finish",
];

#[derive(Debug, FromRequestHead)]
struct Puzzles {
    urls: Urls,
}

impl Puzzles {

}
