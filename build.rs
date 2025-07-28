use std::path::PathBuf;
use imageproc::drawing::{Blend, Canvas};
use imageproc::image::{DynamicImage, ImageReader, RgbaImage};

const CSS_PATH: &str = "static/static/css";

fn main() -> anyhow::Result<()> {
    build_css();
    generate_image()?;

    println!("cargo:rerun-if-changed=build.rs");

    Ok(())
}

fn build_css() {
    const SCSS_FILES: [&str; 4] = [
        "main",
        "finish",
        "sky",
        "keypad",
    ];

    println!("cargo::rerun-if-changed=scss/main.scss");
    println!("cargo::rerun-if-changed=scss/custom.scss");
    println!("cargo::rerun-if-changed=scss/bootstrap-neon-glow.scss");

    let grass_options = grass::Options::default();

    for scss_file in SCSS_FILES {
        let scss_path = format!("scss/{scss_file}.scss");
        let css_path = format!("{CSS_PATH}/{scss_file}.css");

        println!("cargo::rerun-if-changed={scss_path}");

        let mut css = grass::from_path(&scss_path, &grass_options)
            .expect("failed to compile SCSS");

        let build_profile = std::env::var("PROFILE").expect("Cargo should set PROFILE");
        if build_profile == "release" {
            let result = {
                let mut stylesheet = lightningcss::stylesheet::StyleSheet::parse(
                    &css,
                    lightningcss::stylesheet::ParserOptions::default(),
                )
                    .expect("failed to parse CSS");
                stylesheet
                    .minify(lightningcss::stylesheet::MinifyOptions::default())
                    .expect("failed to minify CSS");
                let printer_options = lightningcss::stylesheet::PrinterOptions {
                    minify: true,
                    ..Default::default()
                };
                stylesheet
                    .to_css(printer_options)
                    .expect("failed to print minified CSS")
            };

            css = result.code;
        }

        let out_dir = std::env::var("OUT_DIR").expect("OUT_DIR should be set");
        let css_path = PathBuf::from(out_dir).join(css_path);
        let css_dir = css_path
            .parent()
            .expect("failed to get CSS parent directory");
        std::fs::create_dir_all(css_dir).expect("failed to create CSS directory");
        std::fs::write(css_path, css).expect("failed to write CSS");
    }
}

fn generate_image() -> anyhow::Result<()> {
    let mut img = ImageReader::open("image/img/source.png")?.decode()?;
    let font = std::fs::read("game/utils/fonts/Roboto/Roboto-Black.ttf")?;
    let font = ab_glyph::FontRef::try_from_slice(&font)?;

    let text_scale = ab_glyph::PxScale::from(575.);
    let text = "/h4x.sh/";

    let (w, h) = imageproc::drawing::text_size(text_scale, &font, text);
    let center_w = (img.width() as i32 - w as i32) / 2;
    let center_h = (img.height() as i32 - h as i32) / 2;

    let mut text_image = RgbaImage::new(img.width(), img.height());
    imageproc::drawing::draw_text_mut(&mut text_image, imageproc::image::Rgba([255, 255, 255, 255]), center_w, center_h, text_scale, &font, text);
    text_image.pixels_mut().for_each(|px| {
        px.0[3] = (px.0[3] as f64 * 2. / 255.).round() as u8;
    });
    imageproc::image::imageops::overlay(&mut img, &text_image, 0, 0);

    let out_dir = std::env::var("OUT_DIR").expect("OUT_DIR should be set");
    let img_path = PathBuf::from(out_dir).join("static/static/images/lookatme.png");
    let img_dir = img_path
        .parent()
        .expect("failed to get image parent directory");
    std::fs::create_dir_all(img_dir).expect("failed to create image directory");

    img.save(img_path)?;

    Ok(())
}
