use askama::Template;
use cot::html::Html;
use cot::reverse;

use crate::base_context::BaseContext;

#[derive(Debug, Template)]
#[template(path = "game/hidden_puzzle.html")]
struct HiddenPuzzleTemplate {
    base_context: BaseContext,
    continue_url: String,
}

async fn render_hidden_puzzle(
    base_context: BaseContext,
    continue_url: String,
) -> cot::Result<Html> {
    let template = HiddenPuzzleTemplate {
        base_context,
        continue_url,
    };
    Ok(Html::new(template.render()?))
}

pub async fn terminal_hidden(base_context: BaseContext) -> cot::Result<Html> {
    let continue_url = reverse!(base_context.urls, "terminal")?;
    render_hidden_puzzle(base_context, continue_url).await
}

pub async fn pages_hidden(base_context: BaseContext) -> cot::Result<Html> {
    let continue_url = reverse!(base_context.urls, "pages")?;
    render_hidden_puzzle(base_context, continue_url).await
}
