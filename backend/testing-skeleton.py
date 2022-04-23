import os
import pytest
from pytest import ExitCode

#now we need to run python3 testing-skeleton
def filepath():
    if os.path.basename(os.getcwd()) =="backend":#we are in COSC4p02Project2022/backend
        return "./testingFiles/"
    else:#we are in cosc4p02Project2022
        return "./backend/testingFiles/"

list = [] 
for name in os.listdir(filepath()):
    list.append(filepath()+name)

extc = pytest.main(list)
raise SystemExit(extc)