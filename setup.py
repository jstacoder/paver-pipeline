from setuptools import setup
import json

setup(
    name='paver-pipeline',
    packages=['paver_pipeline'],
    version=(lambda:json.loads(open('version.json','r').read()).get('version'))(),
    author='kyle roux',
    description=('Asset pipeline / builder, similar to '
                 'Grunt, or Gulp, but built with paver and python'),
    url='https://github.com/jstacoder/paver-pipeline',
    author_email='kyle@level2designs.com',
    install_requires=[
        'PyNg-Annotate',        
        'jsmin',
        'ugliPyJs',
        'PyExecjs',
        'coffeescript',
    ]
)
