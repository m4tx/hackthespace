pub(crate) fn current_year() -> i32 {
    <chrono::DateTime<chrono::Utc> as chrono::Datelike>::year(&chrono::Utc::now())
}
