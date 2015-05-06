# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0,os.path.realpath(os.path.dirname(__file__)))
from paver_pipeline._pave import *
from paver_pipeline.git import *
from setuptools.command import *
