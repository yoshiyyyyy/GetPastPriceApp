from flask import Flask,render_template
from flask import request
from .utiliteis.generate_csv import GenerateCsv
from .utiliteis.genarate_line_graph import GenerateLineGraph
import re

#Flaskオブジェクトの生成
app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)
    
