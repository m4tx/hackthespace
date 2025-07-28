const PUZZLE_ORDER: [&str; 13] = [
    "rot13",
    "sky",
    "image",
    "terminal", // Requires hard-coding the next puzzle
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

#[derive(Debug)]
struct Puzzles {}

impl Puzzles {}

#[derive(Debug, Copy, Clone, PartialEq, Eq, Hash)]
enum Puzzle {
    Rot13,
    Sky,
    Image,
    Terminal,
    Redirect,
    Login,
    Pages,
    AudioSpectrum,
    Keypad,
    Vigenere,
    StegoMix,
    Reverse,
    Finish,
}

impl Puzzle {
    fn for_num(num: u32) -> Option<Self> {
        match num {
            0 => Some(Self::Rot13),
            1 => Some(Self::Sky),
            2 => Some(Self::Image),
            3 => Some(Self::Terminal),
            4 => Some(Self::Redirect),
            5 => Some(Self::Login),
            6 => Some(Self::Pages),
            7 => Some(Self::AudioSpectrum),
            8 => Some(Self::Keypad),
            9 => Some(Self::Vigenere),
            10 => Some(Self::StegoMix),
            11 => Some(Self::Reverse),
            12 => Some(Self::Finish),
            _ => None,
        }
    }

    fn num(&self) -> u32 {
        match self {
            Self::Rot13 => 0,
            Self::Sky => 1,
            Self::Image => 2,
            Self::Terminal => 3,
            Self::Redirect => 4,
            Self::Login => 5,
            Self::Pages => 6,
            Self::AudioSpectrum => 7,
            Self::Keypad => 8,
            Self::Vigenere => 9,
            Self::StegoMix => 10,
            Self::Reverse => 11,
            Self::Finish => 12,
        }
    }

    pub fn str_id(&self) -> &'static str {
        match self {
            Self::Rot13 => "",
            Self::Sky => "toomuchwant",
            Self::Image => "lookclosely",
            Self::Terminal => "h4x.sh",        // also f1ndpr1ze.sh/
            Self::Redirect => "wowsuchsecret", // also ysoslow
            Self::Login => "goawayfromhere",
            Self::Pages => "pagelookup", // also weakgravity
            Self::AudioSpectrum => "spacemetal",
            Self::Keypad => "doorkeypad",
            Self::Vigenere => "dramaticvinegar",
            Self::StegoMix => "lookcloser",
            Self::Reverse => "ayeayepatch",
            Self::Finish => "quadrupedpirate",
        }
    }

    pub fn url(&self) -> String {
        let id = self.str_id();
        if id.is_empty() {
            "/".to_string()
        } else {
            format!("/{id}/")
        }
    }
}
