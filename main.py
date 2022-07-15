
from flask import Flask, redirect, request, url_for, render_template
from text_summarizer import TextSummarizer
from utility import Reader

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

summarizer = TextSummarizer()
music = Reader()

# add a counter for number of lines wanted in sentence 
@app.route('/')
def home():
    return render_template("base.html")

@app.route('/summary/', methods=['GET', 'POST'])
def serve_summary():
    content = str(request.form.get('input-text'))
    # print(content)
    # if len(content) == 0:
    #     return redirect(url_for('home'))

    summarized_text = summarizer.summarize(content)
    try:
        music.save(summarized_text)
    except AssertionError:
        return redirect(url_for('home'))

    return render_template("summary.html", summary = summarized_text)

if __name__ == "__main__":
    app.run(debug=True)
