
from flask import Flask, redirect, request, url_for, render_template

# app configuration
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

@app.route("/")
def home():
    return render_template('index.html')

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     return render_template("index.html")

# @app.route('/<word>/')
# def definition(word):
#     current_word = Word(word)
#     if current_word.meanings == 404:
#         return render_template('error.html')
#     else:
#         return render_template('result.html', search_query = current_word)

# running the app
if __name__ == "__main__":
    app.run(debug = True)

