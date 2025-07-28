use askama::Template;
use cot::html::Html;
use hackthespace_core::base_context::BaseContext;

#[derive(Debug, Template)]
#[template(path = "game/hidden_puzzle.html")]
struct HiddenPuzzleTemplate {
    base_context: BaseContext,
}

pub async fn hidden_puzzle(base_context: BaseContext) -> cot::Result<Html> {
    let template = HiddenPuzzleTemplate { base_context };

    Ok(Html::new(template.render()?))
}
