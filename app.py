from __future__ import annotations

import re

from flask import Flask, make_response, render_template, request

app = Flask(__name__)


def format_phone_number(raw_phone: str) -> str:
    """Преобразует номер к формату 8-***-***-**-**."""
    digits = re.sub(r"\D", "", raw_phone)

    # Для себя: если ввели 10 цифр, считаем это номером без ведущей цифры.
    if len(digits) == 10:
        digits = "8" + digits
    elif len(digits) == 11:
        digits = "8" + digits[1:]

    return f"{digits[0]}-{digits[1:4]}-{digits[4:7]}-{digits[7:9]}-{digits[9:11]}"


def validate_phone(raw_phone: str) -> str | None:
    """Возвращает текст ошибки или None, если номер корректен."""
    allowed_pattern = r"^[0-9\s().+\-]+$"
    if not re.match(allowed_pattern, raw_phone):
        return "Недопустимый ввод. В номере телефона встречаются недопустимые символы."

    digits = re.sub(r"\D", "", raw_phone)
    expected_digits = 11 if raw_phone.strip().startswith(("+7", "8")) else 10
    if len(digits) != expected_digits:
        return "Недопустимый ввод. Неверное количество цифр."

    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/request-info")
def request_info():
    return render_template(
        "request_info.html",
        url_params=request.args.items(),
        headers=request.headers.items(),
        cookies=request.cookies.items(),
    )


@app.route("/set-demo-cookie")
def set_demo_cookie():
    response = make_response(render_template("cookie_set.html"))
    response.set_cookie("student_cookie", "flask-lab2-demo", max_age=3600)
    return response


@app.route("/auth-form", methods=["GET", "POST"])
def auth_form():
    if request.method == "POST":
        login = request.form.get("login", "")
        password = request.form.get("password", "")
        return render_template("auth_result.html", login=login, password=password, form_data=request.form.items())

    return render_template("auth_form.html")


@app.route("/phone-check", methods=["GET", "POST"])
def phone_check():
    phone_value = ""
    error_message = None
    formatted_phone = None

    if request.method == "POST":
        phone_value = request.form.get("phone", "")
        error_message = validate_phone(phone_value)
        if not error_message:
            formatted_phone = format_phone_number(phone_value)

    return render_template(
        "phone_check.html",
        phone_value=phone_value,
        error_message=error_message,
        formatted_phone=formatted_phone,
    )


if __name__ == "__main__":
    app.run(debug=True)
