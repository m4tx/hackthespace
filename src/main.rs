mod about;
mod audio_spectrum;
mod base_context;
mod finish;
mod hidden_puzzle;
mod image;
mod keypad;
mod login;
mod migrations;
mod pages;
mod redirect;
mod reverse;
mod rot13;
mod sky;
mod stego_mix;
pub mod template_util;
mod terminal;
mod vigenere;

use cot::bytes::Bytes;
use cot::cli::CliMetadata;
use cot::db::migrations::SyncDynMigration;
use cot::middleware::{AuthMiddleware, LiveReloadMiddleware, SessionMiddleware};
use cot::project::{MiddlewareContext, RegisterAppsContext, RootHandler, RootHandlerBuilder};
use cot::router::{Route, Router};
use cot::static_files::{StaticFile, StaticFilesMiddleware};
use cot::{App, AppBuilder, Project, static_files};

use crate::about::about;
use crate::audio_spectrum::audio_spectrum;
use crate::finish::finish;
use crate::hidden_puzzle::{pages_hidden, terminal_hidden};
use crate::image::image;
use crate::keypad::keypad;
use crate::login::login;
use crate::pages::pages;
use crate::redirect::{redirect, redirect_fail};
use crate::reverse::reverse;
use crate::rot13::rot13;
use crate::sky::sky;
use crate::stego_mix::stego_mix;
use crate::terminal::terminal;
use crate::vigenere::vigenere;

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
            Route::with_handler_and_name("/about/", about, "about"),
            Route::with_handler_and_name("/toomuchwant/", sky, "sky"),
            Route::with_handler_and_name("/lookclosely/", image, "image"),
            Route::with_handler_and_name("/h4x.sh/", terminal, "terminal"),
            Route::with_handler_and_name("/f1ndpr1ze.sh/", terminal_hidden, "terminal_hidden"),
            Route::with_handler_and_name("/wowsuchsecret/", redirect, "redirect"),
            Route::with_handler_and_name("/ysoslow/", redirect_fail, "redirect_fail"),
            Route::with_handler_and_name("/goawayfromhere/", login, "login"),
            Route::with_handler_and_name("/pagelookup/", pages, "pages"),
            Route::with_handler_and_name("/weakgravity/", pages_hidden, "pages_hidden"),
            Route::with_handler_and_name("/spacemetal/", audio_spectrum, "audio_spectrum"),
            Route::with_handler_and_name("/doorkeypad/", keypad, "keypad"),
            Route::with_handler_and_name("/dramaticvinegar/", vigenere, "vigenere"),
            Route::with_handler_and_name("/lookcloser/", stego_mix, "stego_mix"),
            Route::with_handler_and_name("/ayeayepatch/", reverse, "reverse"),
            Route::with_handler_and_name("/quadrupedpirate/", finish, "finish"),
        ])
    }

    fn static_files(&self) -> Vec<StaticFile> {
        let mut files = static_files!(
            "static/images/pirate.png",
            "static/images/omg.png",
            "static/images/surfinginspace.png",
            "static/images/vinegar.png",
            "static/images/finish.png",
            "static/images/generated/lookcloser.jpg",
            "static/audio/deadlyfox.ogg",
            "static/js/terminal.js",
            "static/js/keypad.js",
            "static/vendor/images/ng-background-dot.png",
            "static/vendor/css/jquery.terminal-2.2.0.min.css",
            "static/vendor/js/jquery.terminal-2.2.0.min.js",
            "static/vendor/css/open-iconic-bootstrap.css",
            "static/vendor/fonts/open-iconic.eot",
            "static/vendor/fonts/open-iconic.otf",
            "static/vendor/fonts/open-iconic.svg",
            "static/vendor/fonts/open-iconic.ttf",
            "static/vendor/fonts/open-iconic.woff",
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
