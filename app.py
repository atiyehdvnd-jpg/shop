from flask import Flask, request,redirect, render_template_string, send_from_directory, url_for, session
import os
app = Flask(__name__)
app.secret_key = 'mysecretkey'


@app.route("/", methods=["GET"])
def show_login():
    if session.get("logged_in"):
        return redirect(url_for("show_panel"))
    with open("login.html", encoding="utf-8") as f:
        content = f.read()
    return render_template_string(content.replace("<!-- ERROR_PLACEHOLDER -->", ""))


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if os.path.exists("users.txt"):
        with open("users.txt", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) >= 2:
                    u, p = parts[0], parts[1]
                    role = parts[2] if len(parts) == 3 else "user"
                    if u == username and p == password:
                        session["logged_in"] = True
                        session["role"] = role
                        if role == "admin":
                            return redirect("/panel")
                        else:
                            return redirect("/index")

    with open("login.html", encoding="utf-8") as f:
        html = f.read()
    html = html.replace("<!-- ERROR_PLACEHOLDER -->", "<p style='color:red'>نام کاربری یا رمز اشتباه است ❌</p>")
    return render_template_string(html)


@app.route("/signup", methods=["GET"])
def show_signup():
    with open("signup.html", encoding="utf-8") as f:
        html = f.read()
    return render_template_string(html.replace("<!-- SIGNUP_ERROR_PLACEHOLDER -->", ""))

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    if os.path.exists("users.txt"):
        with open("users.txt", encoding="utf-8") as f:
            for line in f:
              if line.strip().split(":")[0] == username:
                    with open("signup.html", encoding="utf-8") as f2:
                        html = f2.read()
                    html = html.replace("<!-- SIGNUP_ERROR_PLACEHOLDER -->", "<p style='color:red'>این نام کاربری قبلاً ثبت شده است ❌</p>")
                    return render_template_string(html)

    with open("users.txt", "a", encoding="utf-8") as f:
        f.write(f"{username}:{password}:user\n")

    return redirect("/")


@app.route("/panel", methods=["GET"])
def show_panel():
    if not session.get("logged_in"):
        return redirect("/")
    return send_from_directory('.', 'panel.html')


@app.route("/index", methods=["GET"])
def home():
    if not session.get("logged_in"):
        return redirect("/")
    return send_from_directory('.', 'index.html')


@app.route("/<path:filename>")
def serve_files(filename):
    return send_from_directory('.', filename)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)