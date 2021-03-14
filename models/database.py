from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

#DBへの接続情報を定義
#database.pyと同じパスにweight.dbというファイルを絶対パスで定義
databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "weight.db")
#SQLiteを利用して１で定義した絶対パスにDBを構築
engine = create_engine("sqlite:////" + databese_file, convert_unicode=True)
#DB接続用インスタンスを作成
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
#Baseオブジェクトを生成
Base = declarative_base()
#DB情報を流し込み
Base.query = db_session.query_property()

def init_db():
    import models.models
    #テーブルを作成
    Base.metadata.create_all(bind=engine)

#from models.database import init_db
#init_db()
#↑これでDB作成
