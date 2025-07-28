use askama::Template;
use cot::html::Html;
use hackthespace_core::base_context::BaseContext;

#[derive(Debug, Template)]
#[template(path = "rot13/puzzle.html")]
struct Rot13Template {
    base_context: BaseContext,
}

pub async fn rot13(base_context: BaseContext) -> cot::Result<Html> {
    let template = Rot13Template { base_context };

    Ok(Html::new(template.render()?))
}

mod filters {
    use askama::Values;

    pub fn rot_encode(input: impl ToString, _: &dyn Values, offset: u8) -> askama::Result<String> {
        let result = input
            .to_string()
            .chars()
            .map(|c| {
                if c.is_ascii_alphabetic() {
                    let base = if c.is_ascii_uppercase() { 'A' } else { 'a' };
                    let offset = (c as u8 - base as u8 + offset) % 26;
                    (base as u8 + offset) as char
                } else {
                    c
                }
            })
            .collect();
        Ok(result)
    }
}
