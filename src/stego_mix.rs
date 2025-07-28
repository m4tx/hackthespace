use askama::Template;
use cot::html::Html;

use crate::base_context::BaseContext;

#[derive(Debug, Template)]
#[template(path = "stego_mix/puzzle.html")]
struct StegoMixTemplate {
    base_context: BaseContext,
}

pub async fn stego_mix(base_context: BaseContext) -> cot::Result<Html> {
    let template = StegoMixTemplate { base_context };
    Ok(Html::new(template.render()?))
}
