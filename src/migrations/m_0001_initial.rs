#[derive(Debug, Copy, Clone)]
pub struct Migration;

impl ::cot::db::migrations::Migration for Migration {
    const APP_NAME: &'static str = "hackthespace";
    const MIGRATION_NAME: &'static str = "m_0001_initial";
    const DEPENDENCIES: &'static [::cot::db::migrations::MigrationDependency] = &[];
    const OPERATIONS: &'static [::cot::db::migrations::Operation] =
        &[::cot::db::migrations::Operation::create_model()
            .table_name(::cot::db::Identifier::new("hackthespace__page"))
            .fields(&[
                ::cot::db::migrations::Field::new(
                    ::cot::db::Identifier::new("id"),
                    <::cot::db::Auto<i64> as ::cot::db::DatabaseField>::TYPE,
                )
                .auto()
                .primary_key()
                .set_null(<::cot::db::Auto<i64> as ::cot::db::DatabaseField>::NULLABLE),
                ::cot::db::migrations::Field::new(
                    ::cot::db::Identifier::new("url"),
                    <::cot::db::LimitedString<100> as ::cot::db::DatabaseField>::TYPE,
                )
                .set_null(<::cot::db::LimitedString<100> as ::cot::db::DatabaseField>::NULLABLE),
                ::cot::db::migrations::Field::new(
                    ::cot::db::Identifier::new("name"),
                    <::cot::db::LimitedString<100> as ::cot::db::DatabaseField>::TYPE,
                )
                .set_null(<::cot::db::LimitedString<100> as ::cot::db::DatabaseField>::NULLABLE),
                ::cot::db::migrations::Field::new(
                    ::cot::db::Identifier::new("date"),
                    <chrono::DateTime<chrono::FixedOffset> as ::cot::db::DatabaseField>::TYPE,
                )
                .set_null(
                    <chrono::DateTime<chrono::FixedOffset> as ::cot::db::DatabaseField>::NULLABLE,
                ),
            ])
            .build()];
}

#[derive(::core::fmt::Debug)]
#[::cot::db::model(model_type = "migration")]
pub(super) struct _Page {
    #[model(primary_key)]
    pub(super) id: ::cot::db::Auto<i64>,
    pub(super) url: ::cot::db::LimitedString<100>,
    pub(super) name: ::cot::db::LimitedString<100>,
    pub(super) date: ::chrono::DateTime<::chrono::FixedOffset>,
}
