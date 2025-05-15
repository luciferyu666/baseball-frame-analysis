### Endpoints

| Method | Path | Description |
| ------ | ---- | ----------- |
| GET    | /healthz | liveness probe |
| WS     | /ws/live | live JPEG base64 + detections |
| GET    | /events | paginated event list |
| GET    | /frames/{id}.jpg | raw frame file |
