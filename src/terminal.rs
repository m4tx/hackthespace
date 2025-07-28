use askama::Template;
use cot::html::Html;
use hackthespace_core::base_context::BaseContext;

#[derive(Debug, Template)]
#[template(path = "terminal/puzzle.html")]
struct TerminalTemplate {
    base_context: BaseContext,
}

pub async fn terminal(base_context: BaseContext) -> cot::Result<Html> {
    // TODO update jQuery terminal
    let template = TerminalTemplate { base_context };

    Ok(Html::new(template.render()?))
}
