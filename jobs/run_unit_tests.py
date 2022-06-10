import pytest
import os
import sys

os.chdir("..")

# Skip writing pyc files on a readonly filesystem.
sys.dont_write_bytecode = True
retcode = pytest.main([".", "-p", "no:cacheprovider"])
