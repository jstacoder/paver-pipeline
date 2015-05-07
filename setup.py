from setuptools import setup
import json

setup(
    name='paver-pipeline',
    packages=['paver_pipeline'],
    version=(lambda:json.loads(open('version.json','r').read()).get('version'))(),
    author='kyle roux',
    author_email='kyle@level2designs.com',
    install_requires=[
        'PyNg-Annotate',        
        'jsmin',
        'ugliPyJs',
        'PyExecjs',
        'coffeescript',
    ]
)
