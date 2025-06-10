import json, tempfile, os
from integration.aggregator import StreamAggregator
from integration.exporter import export_json

def test_aggregate_export(tmp_path):
    agg=StreamAggregator()
    agg.add_frame(0, detections=[], pose=[], ocr={})
    out_file=tmp_path/"out.json"
    export_json(agg.frames, out_file)
    assert out_file.exists()
    data=json.load(open(out_file))
    assert data[0]["frame_id"]==0
