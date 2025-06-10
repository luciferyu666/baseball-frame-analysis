from common.utils import smooth_coordinates

def test_smoothing():
    coords=[(0,0),(10,10),(20,20)]
    sm=smooth_coordinates(coords,window=2)
    assert sm[1][0]==5
