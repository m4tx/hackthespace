use chrono::DateTime;
use cot::db::{Auto, LimitedString};

use super::m_0001_initial::_Page;

#[derive(Debug, Copy, Clone)]
pub struct Migration;

impl ::cot::db::migrations::Migration for Migration {
    const APP_NAME: &'static str = "hackthespace";
    const MIGRATION_NAME: &'static str = "m_0002_seed";
    const DEPENDENCIES: &'static [::cot::db::migrations::MigrationDependency] =
        &[::cot::db::migrations::MigrationDependency::migration(
            "hackthespace",
            "m_0001_initial",
        )];
    const OPERATIONS: &'static [::cot::db::migrations::Operation] =
        &[::cot::db::migrations::Operation::custom(seed_pages).build()];
}

fn page(url: &str, name: &str, date: &str) -> _Page {
    _Page {
        id: Auto::auto(),
        url: LimitedString::new(url).expect("url fits within limit"),
        name: LimitedString::new(name).expect("name fits within limit"),
        date: DateTime::parse_from_rfc3339(date).expect("valid RFC 3339 date"),
    }
}

#[::cot::db::migrations::migration_op]
async fn seed_pages(ctx: ::cot::db::migrations::MigrationContext<'_>) -> ::cot::db::Result<()> {
    let mut pages = [
        page("/", "rot13", "2026-01-07T09:14:00+00:00"),
        page("/toomuchwant/", "sky", "2026-01-18T16:42:00+00:00"),
        page("/lookclosely/", "image", "2026-02-03T11:25:00+00:00"),
        page("/h4x.sh/", "terminal", "2026-02-14T08:57:00+00:00"),
        page("/wowsuchsecret/", "redirect", "2026-02-28T14:33:00+00:00"),
        page("/goawayfromhere/", "login", "2026-03-09T19:01:00+00:00"),
        page("/pagelookup/", "pages", "2026-03-22T07:48:00+00:00"),
        page(
            "/spacemetal/",
            "audio_spectrum",
            "2026-04-05T13:20:00+00:00",
        ),
    ];
    ctx.db.bulk_insert(&mut pages).await?;
    Ok(())
}
