# -*- coding: utf-8 -*-
from paver.easy import path, options, Bunch, call_task, cmdopts, needs, task, info, sh
from uglipyjs import UglipyJS
from jsmin import jsmin
from coffeescript import compile as coffee_compile

js_data = Bunch(
        files=[],
        dirs=[],
        operations=[],
        data='',
)
css_data = Bunch(
        files=[],
        dirs=[],
        operations=[],
)
options.js_data = js_data
options.css_data = css_data

@task
def a():
    info('calling a, i dont need anyone')

@task
@needs('a')
def b():
    info('calling b, i need a')

@task
@needs('b')
def c():
    info('calling c, i need b')


@task
def d():
    call_task('c')

@task
@cmdopts([
    ('files=','f','concatenate files'),
    ('outfile=','o','output file, default is stdout'),
])
def concat(options):
    files = [options.concat.files]
    out = ''
    info(files)
    for itm in files:
        out += path(itm).text()
    if options.concat.get('outfile',False):
        pth = path(options.concat.outfile)
        pth.touch()
        pth.write_text(out.encode('utf-8'))

    else:
        options.js_data.data = out


@task
def jsmin(options):
    pass
