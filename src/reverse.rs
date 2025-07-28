use askama::Template;
use cot::html::Html;

use crate::base_context::BaseContext;

const KEY: &[u8] = &[
    0x9f, 0xd0, 0x27, 0x60, 0xab, 0x4c, 0xbe, 0xcf, 0x43, 0xe7, 0xd0, 0xe0, 0x1c, 0x75, 0x87, 0x56,
    0x3c,
];

fn encode_url(url: &str, key: &[u8]) -> Vec<u8> {
    url.chars()
        .rev()
        .zip(key.iter())
        .map(|(c, &k)| c as u8 ^ k)
        .collect()
}

#[derive(Debug, Template)]
#[template(path = "reverse/puzzle.html")]
struct ReverseTemplate {
    base_context: BaseContext,
    encoded_url: Vec<u8>,
    key: Vec<u8>,
}

pub async fn reverse(base_context: BaseContext) -> cot::Result<Html> {
    let finish_url = "/quadrupedpirate/";
    let encoded_url = encode_url(finish_url, KEY);
    let template = ReverseTemplate {
        base_context,
        encoded_url,
        key: KEY.to_vec(),
    };
    Ok(Html::new(template.render()?))
}

pub(crate) mod filters {
    use askama::Values;

    #[askama::filter_fn]
    pub fn hexlist(values: &[u8], _: &dyn Values) -> askama::Result<String> {
        Ok(values
            .iter()
            .map(|b| format!("0x{b:02x}"))
            .collect::<Vec<_>>()
            .join(", "))
    }
}
