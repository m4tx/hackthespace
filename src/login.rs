use md5::{Md5, Digest};
use askama::Template;
use cot::common_types::Password;
use cot::form::{Form, FormContext, FormErrorTarget, FormFieldValidationError, FormResult};
use cot::html::Html;
use cot::{reverse_redirect, Method};
use cot::request::Request;
use cot::response::{IntoResponse, Response};
use hackthespace_core::base_context::BaseContext;

const USERNAME: &str = "Cannonbeam";
const PASSWORD: &str = "starjammer";

#[derive(Debug, Form)]
struct LoginForm {
    username: String,
    password: Password,
}

#[derive(Debug, Template)]
#[template(path = "login/puzzle.html")]
struct LoginTemplate {
    base_context: BaseContext,
    form: <LoginForm as Form>::Context,
}

pub async fn login(base_context: BaseContext, mut request: Request) -> cot::Result<Response> {
    let login_form_context = if request.method() == Method::GET {
        LoginForm::build_context(&mut request).await?
    } else if request.method() == Method::POST {
        let login_form = LoginForm::from_request(&mut request).await?;
        match login_form {
            FormResult::Ok(login_form) => {
                // TODO constant time comparison
                if login_form.username == USERNAME && login_form.password.as_str() == PASSWORD {
                    // TODO next puzzle
                    return Ok(reverse_redirect!(base_context.urls, "index")?);
                }

                let mut context = LoginForm::build_context(&mut request).await?;
                context.add_error(
                    FormErrorTarget::Form,
                    FormFieldValidationError::from_static("Invalid username or password"),
                );
                context
            }
            FormResult::ValidationError(context) => context,
        }
    } else {
        panic!("Unexpected request method");
    };

    let template = LoginTemplate {
        base_context,
        form: login_form_context,
    };
    Html::new(template.render()?).into_response()
}

fn md5(input: &str) -> String {
    let mut hasher = Md5::new();
    hasher.update(input.as_bytes());
    let hash = hasher.finalize();

    base16ct::lower::encode_string(&hash)
}
