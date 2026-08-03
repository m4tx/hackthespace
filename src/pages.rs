use askama::Template;
use cot::db::migrations::Migration as _;
use cot::db::{Auto, Database, LimitedString, model};
use cot::html::Html;
use cot::request::extractors::UrlQuery;
use serde::Deserialize;

use crate::base_context::BaseContext;
use crate::migrations;

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

#[derive(Debug, Deserialize)]
pub struct PagesQuery {
    query: Option<String>,
}

async fn setup_puzzle_db() -> cot::Result<Database> {
    let db = Database::new("sqlite::memory:").await?;
    for op in migrations::m_0001_initial::Migration::OPERATIONS {
        op.forwards(&db).await?;
    }
    for op in migrations::m_0002_seed::Migration::OPERATIONS {
        op.forwards(&db).await?;
    }
    Ok(db)
}

pub async fn pages(
    base_context: BaseContext,
    UrlQuery(query): UrlQuery<PagesQuery>,
) -> cot::Result<Html> {
    let mut template = PagesTemplate {
        base_context,
        object_list: vec![],
        query_error: false,
        query: String::new(),
    };

    if let Some(q) = query.query.filter(|q| !q.is_empty()) {
        let db = setup_puzzle_db().await?;
        let sql = format!("SELECT * FROM hackthespace__page WHERE url = '{q}'");
        match db.raw_as::<Page>(&sql).await {
            Ok(results) => {
                template.object_list = results;
                template.query = q;
            }
            Err(_) => {
                template.query_error = true;
            }
        }
    }

    Ok(Html::new(template.render()?))
}
