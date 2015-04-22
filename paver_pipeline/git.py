from paver import easy
from _pave import cache_get,cache_set
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

def commit_repo(msg='xxx'):
    sh(['git','commit','--allow-empty'])

def _push(remote,branch=None):
    if branch is None:
        branch = 'master'
    sh(['git','push',remote,branch])

@easy.task
@easy.cmdopts([
    ('msg=','m','commit message')], 
    share_with=['push_heroku','deploy']
)
def push_github(options):
    _push('github')

@easy.task
@easy.cmdopts([
    ('msg=','m','commit message')],    
    share_with=['push_github','deploy']
)
def push_heroku(options):
    _push('heroku')

@easy.task
@easy.cmdopts([
    ('msg=','m','commit message')],    
    share_with=['push_heroku','push_github']
)
def deploy():
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
    if branch is None:
        branch = options.work_on.branch
    cache_set('PAVER:GIT:BRANCH',branch)
    easy.info('Switching to branch {}'.format(branch))
    sh('git checkout -b {}'.format(branch))

def finish(branch=None):
    if branch is not None:
        sh('git checkout master')
        sh('git merge {}'.format(branch))
        sh('git branch -d {}'.format(branch))
        increment_version()

@easy.task
@easy.cmdopts([
    ('branch=','b','the current branch to merge with master')]
    ,share_with=['work_on']
)
def done(options,branch=None):
    if branch is None:
        branch = cache_get('PAVER:GIT:BRANCH') or options.done.branch 
    finish(branch)

@easy.task
def version():
    easy.info(get_version())

@easy.task
def increment_version():
    version = get_version()
    l,m,s = map(int,version.split('.'))
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
    set_version('.'.join(map(str,[l,m,s])))