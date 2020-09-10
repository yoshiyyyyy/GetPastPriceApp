from flask import Flask,render_template
from flask import request
from .utiliteis.generate_csv import GenerateCsv
from .utiliteis.genarate_line_graph import GenerateLineGraph
import re
from os.path import join, dirname
from celery import Celery
import settings

def make_celery(app):
    celery = Celery(
        app.name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

#Flaskオブジェクトの生成
app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL=settings.REDIS_URL,
    CELERY_RESULT_BACKEND=settings.REDIS_URL
)
celery = make_celery(app)

#「/」へアクセスがあった場合に、「index.html」を返す
@app.route('/')
def index():
    return render_template('index.html')

# POSTの受け取り
@app.route("/search",methods=['POST'])
def post():
    genre_id = request.form['genre']
    search_name = request.form['search_word']
    file_name = request.form['file_name']
    download_csv = GenerateCsv(genre_id, search_name,file_name)
    download_csv.Execute()
    generate_line_graph = GenerateLineGraph(file_name)
    generate_line_graph.Execute()
    return render_template('complete.html')

@celery.task()


if __name__ == "__main__":
    app.run(debug=True)
    
