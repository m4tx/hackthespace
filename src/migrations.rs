pub mod m_0001_initial;
pub mod m_0002_seed;

pub const MIGRATIONS: &[&::cot::db::migrations::SyncDynMigration] =
    &[&m_0001_initial::Migration, &m_0002_seed::Migration];
