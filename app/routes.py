from app import app
from flask import render_template, url_for, send_from_directory
from app.forms import InputForm
from wikisim.model import WikiModel
from . import helpers_methods as hm


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])

def index():
    form = InputForm()
    if form.validate_on_submit():
        article_name= form.inp.data
        cat_name = hm.process_article(article_name)
        img_src = f"img/{article_name}.png"
        wca_src = f"img/{article_name}_wc.png"
        wcc_src = f"img/c/{cat_name}.png"
        return render_template('index.html', title='Home', form=form, img_src=img_src,wca_src=wca_src,wcc_src=wcc_src)

    return render_template('index.html',title='Home',form=form)

@app.route('/img/<path:path>')
def send_js(path):
    return send_from_directory('img', path)



