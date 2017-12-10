import datetime

import requests
from flask import render_template, redirect, request

from app import app

CONNECTED_NODE_CHAIN_ADDRESS = "http://127.0.0.1:8000/chain"
CONNECTED_NODE_NEW_TX_ADDRESS = "http://127.0.0.1:8000//transactions/new"

posts = []


@app.route('/')
def index():
    return render_template('index.html',
                           title='YourNet: Prototype of Decentralized '
                                 'content sharing',
                           posts=posts)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    post_content = request.form["body"]

    author = request.form["author"]

    post_object = {
          'author': author,
          'body': post_content,
          'time': datetime.datetime.now().strftime('%H:%M:%S')
    }

    res = requests.post(CONNECTED_NODE_NEW_TX_ADDRESS,
                        json=post_object,
                        headers={'Content-type': 'application/json'})

    if res.status_code == 201:
        print(res.text)

    posts.append(post_object)

    return redirect('/')


@app.route('/fetch', methods=['POST', 'GET'])
def fetch_posts():
    resp = requests.get(CONNECTED_NODE_CHAIN_ADDRESS)
    if resp.status_code == 200:
        print(resp.content)
    else:
        print("Some Error ocurred while fetching the chain")
