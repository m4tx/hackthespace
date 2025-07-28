mod image;
mod migrations;
mod puzzles;
mod rot13;
mod sky;
pub mod template_util;
mod terminal;
mod hidden_puzzle;
mod redirect;
mod login;
mod pages;

use askama::Template;
use cot::bytes::Bytes;
use cot::cli::CliMetadata;
use cot::db::migrations::SyncDynMigration;
use cot::html::Html;
use cot::middleware::{AuthMiddleware, LiveReloadMiddleware, SessionMiddleware};
use cot::project::{MiddlewareContext, RegisterAppsContext, RootHandler, RootHandlerBuilder};
use cot::request::extractors::StaticFiles;
use cot::router::{Route, Router};
use cot::static_files::{StaticFile, StaticFilesMiddleware};
use cot::{App, AppBuilder, Project, static_files};
use crate::hidden_puzzle::hidden_puzzle;
use crate::image::image;
use crate::login::login;
use crate::pages::pages;
use crate::redirect::{redirect, redirect_fail};
use crate::rot13::rot13;
use crate::sky::sky;
use crate::terminal::terminal;

struct HackthespaceApp;

macro_rules! generated_static {
    ($path:literal) => {
        StaticFile::new(
            $path,
            Bytes::from_static(include_bytes!(concat!(env!("OUT_DIR"), "/static/", $path,))),
        )
    };
}

impl App for HackthespaceApp {
    fn name(&self) -> &'static str {
        env!("CARGO_CRATE_NAME")
    }

    fn migrations(&self) -> Vec<Box<SyncDynMigration>> {
        cot::db::migrations::wrap_migrations(migrations::MIGRATIONS)
    }

    fn router(&self) -> Router {
        Router::with_urls([
            Route::with_handler_and_name("/", rot13, "rot13"),
            Route::with_handler_and_name("/toomuchwant/", sky, "sky"),
            Route::with_handler_and_name("/lookclosely/", image, "image"),
            Route::with_handler_and_name("/h4x.sh/", terminal, "terminal"),
            Route::with_handler_and_name("/f1ndpr1ze.sh/", hidden_puzzle, "terminal_hidden"),
            Route::with_handler_and_name("/wowsuchsecret/", redirect, "redirect"),
            Route::with_handler_and_name("/ysoslow/", redirect_fail, "redirect_fail"),
            Route::with_handler_and_name("/goawayfromhere/", login, "login"),
            Route::with_handler_and_name("/pagelookup/", pages, "pages"),
            Route::with_handler_and_name("/weakgravity/", hidden_puzzle, "pages_hidden"),
        ])
    }

    fn static_files(&self) -> Vec<StaticFile> {
        let mut files = static_files!(
            "static/images/pirate.png",
            "static/images/omg.png",
            "static/js/terminal.js",
            "static/vendor/images/ng-background-dot.png",
            "static/vendor/css/jquery.terminal-2.2.0.min.css",
            "static/vendor/js/jquery.terminal-2.2.0.min.js",
            "static/vendor/css/open-iconic-bootstrap.css",
        );
        files.extend(vec![
            generated_static!("static/css/main.css"),
            generated_static!("static/css/finish.css"),
            generated_static!("static/css/sky.css"),
            generated_static!("static/css/keypad.css"),
            generated_static!("static/images/lookatme.png"),
        ]);
        files
    }
}

struct HackthespaceProject;

impl Project for HackthespaceProject {
    fn cli_metadata(&self) -> CliMetadata {
        cot::cli::metadata!()
    }

    fn register_apps(&self, apps: &mut AppBuilder, _context: &RegisterAppsContext) {
        apps.register_with_views(HackthespaceApp, "");
    }

    fn middlewares(&self, handler: RootHandlerBuilder, context: &MiddlewareContext) -> RootHandler {
        handler
            .middleware(StaticFilesMiddleware::from_context(context))
            .middleware(AuthMiddleware::new())
            .middleware(SessionMiddleware::from_context(context))
            .middleware(LiveReloadMiddleware::from_context(context))
            .build()
    }
}

#[cot::main]
fn main() -> impl Project {
    HackthespaceProject
}
