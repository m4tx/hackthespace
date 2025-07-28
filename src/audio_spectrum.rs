use askama::Template;
use cot::html::Html;

use crate::base_context::BaseContext;

#[derive(Debug, Template)]
#[template(path = "audio_spectrum/puzzle.html")]
struct AudioSpectrumTemplate {
    base_context: BaseContext,
}

pub async fn audio_spectrum(base_context: BaseContext) -> cot::Result<Html> {
    let template = AudioSpectrumTemplate { base_context };
    Ok(Html::new(template.render()?))
}
