#import datetime
#from functools import wraps

from dotenv import find_dotenv, load_dotenv

# from final_project import auth, db, sessions
# from final_project._constants import SECRET_ENV_FILE
# from final_project.sessions import login_required
from flask import Flask, render_template, request  #, g, json, Response, abort

from final_project.__constants import SECRET_ENV_FILE
from final_project.auth import setup_auth
from final_project.compiler import Compiler

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


def index():
    compiler_obj = Compiler()
    program = request.form.get("mips_code")
    print(repr(program))
    # sample programs
    # program = "li $t0 10\nli $t1 5\nmul $t2 $t0 $t1\nmult $t0 $t1"
    # program = "li $t0 4294967295\nli $t1 2\nmult $t0 $t1"
    # program = "li $t0 -17\nli $t1 5\ndiv $t0 $t1"
    # program = "li $t0 10\nli $t1 12\nori $t2 $t0 15"
    # program = "li $t0 10\nsll $t1 $t0 1\nsrl $t2 $t0 1"

    if program:
        compiler_obj.print_registers()
        compiler_obj.compile(program)
        compiler_obj.print_registers()

    registers = compiler_obj.get_registers()

    return render_template("mainScreen.html", 
                            reg_zero = registers["$zero"].get_value(), reg_at = registers["$at"].get_value(),
                            reg_v0 = registers["$v0"].get_value(), reg_v1 = registers["$v1"].get_value(),
                            reg_a0 = registers["$a0"].get_value(), reg_a1 = registers["$a1"].get_value(),
                            reg_a2 = registers["$a2"].get_value(), reg_a3 = registers["$a3"].get_value(),
                            reg_t0 = registers["$t0"].get_value(), reg_t1 = registers["$t1"].get_value(),
                            reg_t2 = registers["$t2"].get_value(), reg_t3 = registers["$t3"].get_value(),
                            reg_t4 = registers["$t4"].get_value(), reg_t5 = registers["$t5"].get_value(),
                            reg_t6 = registers["$t6"].get_value(), reg_t7 = registers["$t7"].get_value(),
                            reg_s0 = registers["$s0"].get_value(), reg_s1 = registers["$s1"].get_value(),
                            reg_s2 = registers["$s2"].get_value(), reg_s3 = registers["$s3"].get_value(),
                            reg_s4 = registers["$s4"].get_value(), reg_s5 = registers["$s5"].get_value(),
                            reg_s6 = registers["$s6"].get_value(), reg_s7 = registers["$s6"].get_value(),
                            reg_t8 = registers["$t8"].get_value(), reg_t9 = registers["$t9"].get_value(),
                            reg_k0 = registers["$k0"].get_value(), reg_k1 = registers["$k1"].get_value(),
                            reg_gp = registers["$gp"].get_value(), reg_sp = registers["$sp"].get_value(),
                            reg_fp = registers["$fp"].get_value(), reg_ra = registers["$ra"].get_value(),
                            reg_pc = registers["$pc"].get_value(), reg_hi = registers["$hi"].get_value(),
                            reg_lo = registers["$lo"].get_value()
                            )

def loginScreen():
    return render_template("loginScreen.html")

def accountScreen():
    return render_template("accountScreen.html")



@login_required
def account():
    return render_template("account.html")

def setup_routes(app):
    app.route("/", methods = ["GET", "POST"])(index)
    app.route("/loginScreen")(loginScreen)
    app.route("/accountScreen")(accountScreen)
    app.route("/account")(account)

def run_app(debug: bool = True) -> None:
    app = create_app()
    app.run(debug=debug)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
