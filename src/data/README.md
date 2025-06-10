
# Data Directory

This package provides a standardised layout and helper functions (`data.paths`)
for managing all datasets, outputs and model weights.

```
from data import paths
paths.ensure_dirs()
video_path = paths.raw("game1.mp4")
json_output = paths.json_out("game1_events.json")
```
