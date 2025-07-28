use askama::Template;
use cot::html::Html;

use crate::base_context::BaseContext;

#[derive(Debug, Template)]
#[template(path = "about.html")]
struct AboutTemplate {
    base_context: BaseContext,
}

pub async fn about(base_context: BaseContext) -> cot::Result<Html> {
    let template = AboutTemplate { base_context };

    Ok(Html::new(template.render()?))
}
