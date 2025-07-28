use askama::Template;
use cot::html::Html;
use hackthespace_core::base_context::BaseContext;

#[derive(Debug, Template)]
#[template(path = "image/puzzle.html")]
struct ImageTemplate {
    base_context: BaseContext,
}

pub async fn image(base_context: BaseContext) -> cot::Result<Html> {
    let template = ImageTemplate { base_context };

    Ok(Html::new(template.render()?))
}
