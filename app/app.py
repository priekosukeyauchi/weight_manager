import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
import datetime
from flask import Flask, render_template, request, session, redirect, url_for
#ログインに必要なライブラリ
from models.models import User
from models.models import Weight
from app import key
from hashlib import sha256
from models.database import db_session


app = Flask(__name__)
app.secret_key = key.SECRET_KEY

@app.route("/")
def index():
    if "user_name" in session:
        name = session["user_name"]
        return render_template("index.html", name=name)
    else:
        return redirect(url_for("top", status="logout"))

@app.route("/top")
def top():
    status = request.args.get("status")
    return render_template("top.html", status=status)

@app.route("/login", methods=["POST"])
def login():
    #フォームに入力されたユーザー名を取得
    user_name = request.form["user_name"]
    #ユーザー名を持つDBレコードをuserテーブルから抽出
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        #フォームに入力されたパスワードを取得
        password = request.form["password"]
        #ハッシュ化
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8"))
        #DBレコードのハッシュ化パスワードと一致するかどうか判定
        if user.hashed_password == hashed_password:
            session["user_name"] = user_name
            return redirect(url_for("register"))
        else:
            return redirect(url_for("top", status="wrong_password"))
    else:
        return redirect(url_for("top", status="user_notfound"))

@app.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("top", status="logout"))

@app.route("/newcomer")
def newcomer():
    status = request.args.get("status")
    return render_template("newcomer.html", status=status)

@app.route("/registar",methods=["POST"])
def registar():
    global user_name
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        return redirect(url_for("newcomer",status="exist_user"))
    else:
        global height
        global target
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        height = request.form["height"]
        target = request.form["target"] 
        user = User(user_name, hashed_password, height, target)
        db_session.add(user)
        db_session.commit()
        session["user_name"] = user_name
        return redirect(url_for("index"))

@app.route("/record", methods=["post"])
def weight_bmi():
    info = db_session.query(User).filter_by(user_name="rieko")
    for i in info:
        user_name = i.user_name
        target = int(i.target_weight )
        date = datetime.datetime.now()
        weight= int(request.form["weight_in"])
        height = i.height
        bmi = weight/ (int(height)/100)**2
        difference = weight - target

        weight = Weight(user_name, date, weight, bmi, difference)
        db_session.add(weight)
        db_session.commit()
        session["user_name"] = user_name
        return redirect(url_for("index"))
    
    
    

    """graph = plt.plot(read_df["日付(年/月/日/時/分)"], read_df["目標体重との差(kg)"], label="difference(kg)", color = "r")
    plt.title("weight_difference")
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.ylabel("difference(kg)")

    xmin, xmax = 0, len(read_df)
    plt.hlines(0, xmin, xmax, "black", linestyles="dashed")

    plt.hlines(1, xmin, xmax, "blue", linestyles="dashed")
    plt.hlines(-1, xmin, xmax, "blue", linestyles="dashed")

    plt.savefig("./static/img/weight_difference.png")

    return redirect(url_for("index"))"""

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

#メインとなる部分
if __name__ == "__main__":
    app.run(debug=True)
  

