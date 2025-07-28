use askama::Template;
use cot::html::Html;

use crate::base_context::BaseContext;

#[derive(Debug, Template)]
#[template(path = "vigenere/puzzle.html")]
struct VigenereTemplate {
    base_context: BaseContext,
}

pub async fn vigenere(base_context: BaseContext) -> cot::Result<Html> {
    let template = VigenereTemplate { base_context };
    Ok(Html::new(template.render()?))
}

pub(crate) mod filters {
    use askama::Values;

    #[askama::filter_fn]
    pub fn vigenere(input: impl ToString, _: &dyn Values, key: &str) -> askama::Result<String> {
        let key = key.to_lowercase();
        let key_bytes: Vec<u8> = key.bytes().collect();
        let mut result = String::new();
        let mut key_index = 0;

        for c in input.to_string().chars() {
            if c.is_ascii_alphabetic() {
                let base = if c.is_ascii_uppercase() { b'A' } else { b'a' };
                let shift = key_bytes[key_index % key_bytes.len()] - b'a';
                let encoded = (c as u8 - base + shift) % 26 + base;
                result.push(encoded as char);
                key_index += 1;
            } else {
                result.push(c);
            }
        }

        Ok(result)
    }
}
