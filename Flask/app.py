from flask import Flask, render_template, url_for, request, redirect, session, json
from pickle import load
from subprocess import call
from os import getcwd,path
import sys
src_path = path.join(getcwd(),'source')
sys.path.append(src_path)
import fetcher as F

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def fetch_from_file():
    fl_path = path.join(src_path,'temp\\data.pkl')
    with open(fl_path,'rb') as f:
        contests = load(f)
    return contests

@app.route('/fetch', methods=['POST'])
def fetch_data():
    F.fetch()
    result = fetch_from_file()
    session['all_contests'] = json.dumps(result, default=lambda o: o.__dict__)
    return redirect(url_for('page'))


@app.route('/')
def page():
    all_contests = session.pop('all_contests',None)
    if all_contests:
        all_contests = json.loads(all_contests)
    return render_template("page.html",all_contests = all_contests)

if __name__ == '__main__':
    app.run()