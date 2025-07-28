use cot::db::{model, Auto, LimitedString};
use askama::Template;
use cot::html::Html;
use hackthespace_core::base_context::BaseContext;

#[derive(Debug, Clone, PartialEq, Eq)]
#[model]
struct Page {
    #[model(primary_key)]
    id: Auto<i64>,
    url: LimitedString<100>,
    name: LimitedString<100>,
    date: chrono::DateTime<chrono::FixedOffset>,
}

#[derive(Debug, Template)]
#[template(path = "pages/puzzle.html")]
struct PagesTemplate {
    base_context: BaseContext,
    object_list: Vec<Page>,
    query_error: bool,
    query: String,
}

pub async fn pages(base_context: BaseContext) -> cot::Result<Html> {
    let template = PagesTemplate { base_context, object_list: vec![], query_error: false, query: String::new() };

    Ok(Html::new(template.render()?))
}
