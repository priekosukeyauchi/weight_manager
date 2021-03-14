#webサーバーを立ち上げるときに実行するファイル

from app.app import app
if __name__=="__main__":
    app.run(debug=True)