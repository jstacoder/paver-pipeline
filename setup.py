from setuptools import setup

setup(
    name='paver-pipeline',
    packages=['paver_pipeline'],
    version='0.0.4',
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
