import json
import os
from paver import easy,options
from paver.easy import path,sh
from paver.options import Bunch  
try:
    from jsmin import jsmin
except ImportError:
    jsmin = None
try:
    from coffeescript import compile as compile_coffee
except ImportError:
    compile_coffee = None
try:
    from uglipyjs import compile as uglify
except ImportError:
    uglify = None

options.assets = Bunch(
    css='',
    js='',
    folders=Bunch(
        js='src',
        css='static/css',
    ),
    js_files=[],
    js_ext='.coffee',
    css_ext='.css',
    outfiles=Bunch(
        prod=Bunch(
            js='vendor/app.min.js',
            css=''
        ),
        dev=Bunch(
            js='vendor/app.js',
            css=''
        )            
    ),
)

options.build = Bunch(
    buildtype=None,    
)

def _show_files():
    map(lambda x: easy.info(x[1]),options.assets.js_files)
    
def _get_files(root,ext=None,recurse=False):
    if not recurse:
        file_list = easy.path(root).files() if easy.path(root).exists() else None
    else:
       file_list =  list(easy.path(root).walkfiles()) if easy.path(root).exists() else None
    if file_list is not None:
        return file_list if ext is None else [f for f in file_list if file_list and any(map(lambda x: f.endswith(x),ext))]
    else:
        return []

def _get_buildtype():
    return options.build.buildtype or os.environ.get('BUILD_TYPE')                                            

@easy.task
def get_js():
    '''
        gather all source js files, or some other precompiled source files
                     to gather files other than javascript, set:                     
                        options.assets.js_ext
                        
                     to the extension to collect ie for coffeescript:                     
                        options.assets.js_ext = '.coffee'
                        
    '''
    ext = options.assets.js_ext or '.js'
    files = _get_files(options.assets.folders.js,ext,True)    
    options.assets.js_files = map(lambda x: (str(x),x.text()),files)    

@easy.task
def get_css():
    '''
        gather all source css files, or some other precompiled source files
                     to gather files other than css files, set:                     
                        options.assets.css_ext
                        
                     to the extension to collect ie for less:                     
                        options.assets.css_ext = '.less'\n                                            
    '''
    ext = options.assets.css_ext or '.css'
    files = _get_files(options.assets.folders.css,ext,True)
    options.assets.css_files = map(lambda x: (str(x),x.text()),files)        

@easy.task
@easy.needs('get_js')
def coffee():
    '''
        compile coffeescript files into javascript
    '''
    if compile_coffee is None:
        easy.info('coffee-script not installed! cannot compile coffescript')
        return None
    options.assets.js_files = map(lambda x: ((x[0],compile_coffee(x[1],True))),options.assets.js_files)    
        
@easy.task
def write_js(buildtype=None):
    '''
        write out all gathered javascript to the file specified in options.assets.outfiles[BUILD_TYPE].js
    '''
    if not easy.path('vendor').exists():
        easy.info('making vendor dir')
        os.mkdir('vendor')
    buildtype = buildtype or _get_buildtype()    
    with open(options.assets.outfiles[buildtype].js,'w') as f:
        f.write(options.assets.js)
        easy.info('Wrote file: {}'.format(options.assets.outfiles[buildtype].js))

@easy.task
def minify():
    '''
        minify javascript source with the jsmin module
    '''
    if jsmin is None:
        easy.info('Jsmin not installed! cannot minify code')
        return None
    options.assets.js_files = map(lambda x: ((x[0],jsmin(x[1]))),options.assets.js_files)

@easy.task
def uglifyjs():
    '''
        uglify javascript source code (obstification) using the ugliPyJs module
    '''
    if uglify is None:
        easy.info('ugliPyJs not installed! cannot uglify code')
        return None
    for fle,data in options.assets.js_files:
        try:
            options.assets.js_files[options.assets.js_files.index((fle,data))] = (fle,uglify(data))
        except Exception, e:
            print e.message             

@easy.task
def concat():
    '''
        concatenate all javascript files currently in memory
    '''
    options.assets.js = ''.join(map(lambda x: str(x[1]),options.assets.js_files))
    
@easy.task
def build_production():
    '''
        Full Build: gather js or coffeescript, compile coffeescript, uglify, minify, concat, write out
    '''
    get_js()
    coffee()
    uglifyjs()
    minify()
    concat()
    write_js()

@easy.task
def build_dev():
    '''
        Partial Build: gather js or coffeescript, compile coffeescript, concat, write out
    '''
    get_js()
    coffee()
    concat()
    write_js()
    
@easy.task
@easy.cmdopts([
 ('buildtype=','t','build type')
])
def build(options):
    '''
        Run Build, defaults to 'dev'
    '''
    if(not hasattr(options,'build') or (options.build.get('buildtype',None) is None)):
        buildtype = 'dev'        
    else:
        buildtype = options.build.buildtype
    os.environ['BUILD_TYPE'] = buildtype
    dict(
        dev=build_dev,
        prod=build_production,
    )[buildtype]()
    
@easy.task
def run():
    '''
        Run production build and pipe generated js into nodejs for execution
    '''
    options.build = Bunch()
    buildtype = options.build.buildtype = 'prod'
    build(options)
    sh("nodejs {}".format(options.assets.outfiles[buildtype].js))