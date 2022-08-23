# Test each of the transform functions.
import pytest


@pytest.fixture
def return_true():
    return True


@pytest.fixture
def return_false():
    return False

  
def test_true(return_true):
    assert return_true != True

def test_false(return_false):
    assert return_false == False

