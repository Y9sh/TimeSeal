import inspect

def print_line(desc,*args):
    line  = inspect.currentframe().f_back.f_lineno
    file = inspect.stack()[1].filename
    print(f"Current line is {line} at {file} - {desc} ----{args}")