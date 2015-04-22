# coding: utf-8
import paver 

from importlib import import_module

def set_global(name,value):
    globals()[name] = value
    
def load_paver_tasks(module):
    filter(
            None,map(
                lambda x: set_global(
                    x.__name__,x
                ),filter(
                    lambda x: x.__class__ == paver.tasks.Task,
                    map(
                        lambda x: getattr(
                            import_module(
                                module
                            ),x
                        ),dir(
                            import_module(
                                module
                            )
                        )
                    )
                )
            )
        )
    return globals()


if __name__ == "__main__":
    for name,itm in load_paver_tasks('_pave').items():
        globals()[name] = itm

    print globals().keys()
