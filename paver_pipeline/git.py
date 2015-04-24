from paver import easy
import os
from paver.easy import sh
from functools import partial
import json
try:
    from redis import Redis
except ImportError:
    Redis = None
    class Cache(object):
        def __init__(self):
            self.cache = {}

        def get(self,key):
            return self.cache.get(key) if key in self.cache.keys() else None
        def set(self,key,val,*args,**kwargs):
            self.cache[key] = val
            return True
      
cache = Redis() if Redis is not None else Cache()

SET_ARG = dict(ex=7200)

cache_set = lambda key,val: cache.set(key,val,**SET_ARG)
cache_get = lambda key: cache.get(key)

_git = lambda *cmds: sh(['git'] + list(cmds))

def commit_repo(msg=''):
    _git('commit','--allow-empty','-m',msg)

def _push(remote,branch=None):
    if branch is None:
        branch = 'master'
    _git('push',remote,branch)

@easy.task
def push_github(options):
    '''
        push repo to github
    '''
    _push('github')

@easy.task
def push_heroku(options):
    '''
        push repo to heroku 
    '''
    _push('heroku')

@easy.task
@easy.cmdopts([
    ('msg=','m','commit message')
])
def deploy():
    '''
        commit current state and push to github and heroku
    '''
    commit_repo(options.deploy.msg)
    push_github()
    push_heroku()

def get_version():
    return json.loads(open('version.json','r').read()).get('version')

def set_version(version):
    print 'setting version to {}'.format(version)
    with open('version.json','w') as f:
        f.write(json.dumps(dict(version=version)))

@easy.task
@easy.cmdopts([
    ('branch=','b','a new branch to create to work on')],
    share_with=['done'])
def work_on(options,branch=None):
    '''
        create a new working branch and switch to it
    '''
    if branch is None:
        branch = options.work_on.branch
    cache_set('PAVER:GIT:BRANCH',branch)
    easy.info('Switching to branch {}'.format(branch))
    _git('checkout','-b','{}'.format(branch))

def finish(branch=None):
    if branch is not None:
        _git('checkout','master')
        _git('merge','{}'.format(branch))
        _git('branch','-d','{}'.format(branch))
        increment_version()

@easy.task
@easy.cmdopts([
    ('branch=','b','the current branch to merge with master')]
    ,share_with=['work_on']
)
def done(options,branch=None):
    '''
        merge current branch with master, delete working branch and increment project version
    '''
    if branch is None:
        branch = cache_get('PAVER:GIT:BRANCH') or options.done.branch 
    finish(branch)

@easy.task
def version():
    '''
        show local version info
    '''
    easy.info(get_version())

@easy.task
@easy.cmdopts([
    ('minor','m','minor version update'),
    ('mid','i','increment the mid version number'),
    ('major','a','increment major version number'),
])
def increment_version(options):
    '''
        increment local version
    '''
    ver = 'minor' if not bool(options.increment_version) else options.increment_version.keys()[0]
    version = get_version()
    l,m,s = map(int,version.split('.'))
    if ver == 'minor':
        if s == 9:
            s = 0
            if m == 9:
                m = 0
                if str(l).endswith == '9':
                    l = (int(l[0]) + 1) + 0
                else:
                    l += 1
            else:
                m += 1
        else:
            s += 1
    elif ver == 'mid':
        s = 0
        if m == 9:
            m == 0
            if str(l).endswith == '9':
                l = (int(l[0]) + 1) + 0
            else:
                l += 1
        else:
            m += 1
    else:
        s = 0
        m = 0
        if str(l).endswith == '9':
            l = (int(l[0]) + 1) + 0
        else:
            l += 1        
    set_version('.'.join(map(str,[l,m,s])))

@easy.task
@easy.cmdopts([
    ('filename=','f','file to add')    
])
def commit_last_file(options):
    '''
        add last working file to git repo,commit
    '''
    print options.commit_last_file
    _git('add',options.commit_last_file.filename)
    _git('commit','-m','added work')
    _git('push','github','master')
