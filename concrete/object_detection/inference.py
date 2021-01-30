"""
    Inference
"""
print( __package__ )
from cli.examples import hello

def inference() -> int:
    """
        Inference
    """
    print( hello() )
    return 1
