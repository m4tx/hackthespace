use std::fmt::{Display, Formatter};
use std::ops::RangeInclusive;
use askama::filters::Safe;
use askama::Template;
use cot::html::Html;
use cot::request::extractors::StaticFiles;
use cot::router::Urls;
use rand::seq::{IndexedRandom, IteratorRandom};
use hackthespace_core::base_context::BaseContext;

#[derive(Debug, Template)]
#[template(path = "sky/puzzle.html")]
struct SkyTemplate {
base_context: BaseContext
}

pub async fn sky(base_context: BaseContext) -> cot::Result<Html> {
    let template = SkyTemplate {
        base_context
    };

    Ok(Html::new(template.render()?))
}

const CHARS: &str = ".,✦*˚";
const SPACE: &str = "&nbsp;";
const ITEM_NUM: usize = 100;
const SPACE_BETWEEN_LEN_RANGE: RangeInclusive<i32> = 22..=56;

fn generate_sky() -> Safe<String> {
    let mut sky = String::new();
    let chosen = rand::random_range(0..ITEM_NUM);

    for i in 0..ITEM_NUM {
        sky.push_str(&format!("<span style=\"color: #{}\">", rand_gray()));
        if i == chosen {
            sky.push_str(&format!("<a href=\"{}\">★</a>", "TODO"));
        } else {
            sky.push(CHARS.chars().choose(&mut rand::rng()).expect("Failed to choose a character"));
        }
        sky.push_str("</span>");

        for _ in 0..rand::random_range(SPACE_BETWEEN_LEN_RANGE) {
            sky.push_str(SPACE);
            if rand::random_bool(0.5) {
                sky.push(' ');
            }
        }
    }

    Safe(sky)
}

fn rand_gray() -> HexColor {
    let color = rand::random_range(100..=255);
    HexColor::new(color, color, color)
}

#[derive(Debug, Copy, Clone, PartialEq, Eq, Hash)]
struct HexColor(u8, u8, u8);

impl HexColor {
    #[must_use]
    fn new(r: u8, g: u8, b: u8) -> Self {
        HexColor(r, g, b)
    }
}

impl Display for HexColor {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "#{:02X}{:02X}{:02X}", self.0, self.1, self.2)
    }
}
