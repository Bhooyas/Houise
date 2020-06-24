import sys
from io import StringIO
import contextlib

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def execute_return(code):
    try:
        compile(code,'<stdin>','eval')
    except SyntaxError:
        return run
    return eval

def run(code):
    with stdoutIO() as s:
        try:
            exec(code)
        except Exception as e:
            return (e.__class__.__name__+str(e))
    return s.getvalue()

def execute(code):
    try:
        val = execute_return(code)(code)
    except Exception as e:
        val = e.__class__.__name__+str(e)
    if val is not None:
        return val

code = """for i in range(10):print(i)"""
