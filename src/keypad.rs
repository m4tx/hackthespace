use askama::Template;
use cot::form::{Form, FormResult};
use cot::html::Html;
use cot::request::Request;
use cot::response::{IntoResponse, Response};
use cot::{Method, reverse_redirect};

use crate::base_context::BaseContext;

const CORRECT_CODE: &str = "4254292";

#[derive(Debug, Form)]
struct KeypadForm {
    #[form(opts(max_length = 7))]
    code: String,
}

#[derive(Debug, Template)]
#[template(path = "keypad/puzzle.html")]
struct KeypadTemplate {
    base_context: BaseContext,
}

pub async fn keypad(base_context: BaseContext, mut request: Request) -> cot::Result<Response> {
    if request.method() == Method::POST {
        let form = KeypadForm::from_request(&mut request).await?;
        if let FormResult::Ok(form) = form
            && form.code == CORRECT_CODE
        {
            return Ok(reverse_redirect!(base_context.urls, "vigenere")?);
        }
    }

    Html::new(KeypadTemplate { base_context }.render()?).into_response()
}
