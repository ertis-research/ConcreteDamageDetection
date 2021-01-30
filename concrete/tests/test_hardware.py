"""
    Hardware Tests
"""
import torch
import pytest


def test_gpu():
    """
        Check GPU availability
    """
    if torch.cuda.is_available():

        for i in range(torch.cuda.device_count()):

            print("GPU: {}".format(torch.cuda.get_device_name(i)))
    else:

        pytest.fail("GPU Not Configured.")
