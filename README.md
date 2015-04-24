##Paver-Pipeline : <small>v0.0.3</small>

###Tools to make projects easier


_includes_:
*   `paver_pipeline.git` - helpers for managing your git repos
    -  *GitHelpers*: 
        *   commit_file - add a file to your current branchs staging and commit
        *   push_github - push changes to github remote
        *   push_heroku - push changes to heroku remote
        *   deploy      - commit changes and push to heroku and github
    -  *VersionHelpers*:
        *   version - show current version
        *   increment_version - add to current version number
    -  *TimeSavers*:
        *   work_on - create new working branch and store in memory
        *   done - merge working branch with master, delete branch,  and increment project version

To use:

####adding pip installation instructions soon

```bash
git clone https://github.com/jstacoder/paver-pipeline.git
cd paver-pipeline
sudo python setup.py install
```
Then in your projects create a file called `pavement.py` and in it put:

```bash
from paver_pipeline import *
```
and to see what paver commands you can use:

```bash
paver -h
```
