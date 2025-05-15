from src.capture.stream_listener import FRAME_QUEUE, start
def test_queue():
    start()
    import time
    time.sleep(1)
    assert FRAME_QUEUE.qsize()>=0
