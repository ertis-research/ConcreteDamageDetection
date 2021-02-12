"""
    Inference
"""
print( __package__ )
from concrete.cli.examples import hello

def inference() -> int:
    """
        Inference
    """
    print( hello() )
    return 1
