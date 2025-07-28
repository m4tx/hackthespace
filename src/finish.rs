use askama::Template;
use cot::html::Html;

use crate::base_context::BaseContext;

#[derive(Debug, Template)]
#[template(path = "finish/puzzle.html")]
struct FinishTemplate {
    base_context: BaseContext,
}

pub async fn finish(base_context: BaseContext) -> cot::Result<Html> {
    let template = FinishTemplate { base_context };
    Ok(Html::new(template.render()?))
}
