#import datetime
#from functools import wraps

from dotenv import find_dotenv, load_dotenv

# from final_project import auth, db, sessions
# from final_project._constants import SECRET_ENV_FILE
# from final_project.sessions import login_required
from flask import Flask, abort, render_template  #, g, json, request, Response, abort

from final_project.__constants import SECRET_ENV_FILE
from final_project.auth import setup_auth
from final_project.compiler import Compiler

#from flask_restful import Resource, reqparse
#from cs188_a3.__constants import PROJECT_ROOT
#import os
#from final_project.db import Database
#from flask_bcrypt import Bcrypt
#import datetime #for storing timestamps of messages and fronts
from final_project.db import setup_for_app
from final_project.sessions import login_required, setup_sessions


def create_app(dbName = "testing.db"):
    load_dotenv(find_dotenv(SECRET_ENV_FILE))
    app = Flask(__name__)
    setup_for_app(app)
    setup_sessions(app)
    setup_auth(app)
    setup_routes(app)
    return app


def mainScreen():
    return render_template("mainScreen.html")

def loginScreen():
    return render_template("loginScreen.html")

def accountScreen():
    return render_template("accountScreen.html")

def hello():
    compiler_obj = Compiler()
    # program = "li $t0 10\nli $t1 5\nmul $t2 $t0 $t1\nmult $t0 $t1"
    # program = "li $t0 4294967295\nli $t1 2\nmult $t0 $t1"
    # program = "li $t0 -17\nli $t1 5\ndiv $t0 $t1"
    # program = "li $t0 10\nli $t1 12\nori $t2 $t0 15"
    program = "li $t0 10\nsll $t1 $t0 1\nsrl $t2 $t0 1"

    compiler_obj.print_registers()
    compiler_obj.compile(program)
    compiler_obj.print_registers()

    return render_template("hello.html")

@login_required
def account():
    return render_template("account.html")

def setup_routes(app):
    app.route("/")(mainScreen)
    app.route("/loginScreen")(loginScreen)
    app.route("/accountScreen")(accountScreen)

    app.route("/")(index)
    app.route("/hello")(hello)
    app.route("/account")(account)

def run_app(debug: bool = True) -> None:
    app = create_app()
    app.run(debug=debug)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

def index():
    return render_template("index.html")
