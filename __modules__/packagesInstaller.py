# -*- coding: utf-8 -*-
"""

@author: Олег Дмитренко
"""

import sys
import importlib
import subprocess

stdOutput = open("outlog.log", "a")
sys.stderr = stdOutput
sys.stdout = stdOutput

def setup_packeges(packages):
    for package in packages:
        if package in sys.modules:
            print(f"{package!r} already in sys.modules")
            continue
        elif (importlib.util.find_spec(package)) is not None:
            # If you choose to perform the actual import ...
            module = importlib.util.module_from_spec(importlib.util.find_spec(package))
            sys.modules[package] = module
            (importlib.util.find_spec(package)).loader.exec_module(module)
            print(f"{package!r} has been imported")
        else:
            print(f"Can't find the {package!r} module")
            try:
                # implement pip as a subprocess:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            except:
                pass
