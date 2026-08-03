use cot::request::extractors::{FromRequestHead, StaticFiles};
use cot::router::Urls;

#[derive(Debug, FromRequestHead)]
pub struct BaseContext {
    pub static_files: StaticFiles,
    pub urls: Urls,
}
