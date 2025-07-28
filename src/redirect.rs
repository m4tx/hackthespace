use askama::Template;
use cot::html::Html;
use hackthespace_core::base_context::BaseContext;

#[derive(Debug, Template)]
#[template(path = "redirect/puzzle.html")]
struct RedirectTemplate {
    base_context: BaseContext,
}

pub async fn redirect(base_context: BaseContext) -> cot::Result<Html> {
    let template = RedirectTemplate { base_context };

    Ok(Html::new(template.render()?))
}

#[derive(Debug, Template)]
#[template(path = "redirect/fail.html")]
struct RedirectFailTemplate {
    base_context: BaseContext,
}

pub async fn redirect_fail(base_context: BaseContext) -> cot::Result<Html> {
    let template = RedirectFailTemplate { base_context };

    Ok(Html::new(template.render()?))
}
