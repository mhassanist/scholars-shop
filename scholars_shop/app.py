from flask import Flask, render_template, redirect, url_for, request
import sqlite3


app = Flask(__name__)

@app.route('/')
def home():
    return "<p>Hello,</p>"

