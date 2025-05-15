import cv2
def draw(frame, detections, tracks):
    for det in detections:
        x1,y1,x2,y2 = det['bbox']
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
    for oid,cent in tracks.items():
        cv2.circle(frame, tuple(int(c) for c in cent), 4, (0,0,255), -1)
        cv2.putText(frame, f"ID {oid}", tuple(int(c)-10 for c in cent), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,255),1)
    return frame
