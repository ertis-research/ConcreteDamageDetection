"""
    Basic Tests
"""
from cli import examples
from object_detection import inference


def test_1():
    """
        Test 1
    """
    assert 1


def test_modules():
    """
        Test
    """
    assert examples.hello() == "Hello", "Something is wrong"

def test_inference():
    """
        Test
    """
    assert inference.inference() == 1, "Something was wrong"
