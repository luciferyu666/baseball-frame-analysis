import cv2, base64, queue, asyncio
from fastapi import FastAPI, WebSocket
from starlette.responses import FileResponse
from src.capture.stream_listener import FRAME_QUEUE, start as start_capture
from src.analysis.inference import detect_ball
from src.analysis.tracker import CentroidTracker
from src.annotation.overlay import draw
from src.annotation.event_logger import log
from src.storage.local_io import save
from src.utils.scheduler import start as scheduler_start
from src.api.routes import router as event_router

app = FastAPI(title="Baseball Frame API")
app.include_router(event_router)

start_capture()
scheduler_start()
tracker = CentroidTracker()

@app.get("/healthz")
def healthz():
    return {"status":"ok"}

@app.websocket("/ws/live")
async def ws_live(ws:WebSocket):
    await ws.accept()
    frame_id=0
    while True:
        try:
            frame = FRAME_QUEUE.get(timeout=1)
        except queue.Empty:
            await asyncio.sleep(0.01)
            continue
        detections = detect_ball(frame)
        tracks = tracker.update([(d["bbox"],d["conf"]) for d in detections])
        overlay = draw(frame.copy(), detections, tracks)
        path = save(overlay, "live")
        log(frame_id, detections, tracks)
        _, jpg = cv2.imencode(".jpg", overlay)
        b64 = base64.b64encode(jpg.tobytes()).decode()
        await ws.send_json({"frame_id":frame_id,"image":b64,"detections":detections})
        frame_id+=1

@app.get("/frames/{fname}")
def get_frame(fname:str):
    return FileResponse(path=f"outputs/{fname}")
