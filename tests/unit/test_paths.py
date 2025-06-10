from data import paths

def test_paths():
    paths.ensure_dirs()
    p = paths.raw("unit_test.mp4")
    assert "raw" in str(p)
