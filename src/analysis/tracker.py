from collections import OrderedDict
import numpy as np
class CentroidTracker:
    def __init__(self, max_disappeared=20):
        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        self.max_disappeared = max_disappeared
    def register(self, centroid):
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1
    def deregister(self, objectID):
        del self.objects[objectID]
        del self.disappeared[objectID]
    def update(self, detections):
        if len(detections) == 0:
            for oid in list(self.disappeared.keys()):
                self.disappeared[oid] +=1
                if self.disappeared[oid] > self.max_disappeared:
                    self.deregister(oid)
            return self.objects
        input_centroids = np.array([[ (bb[0]+bb[2])//2, (bb[1]+bb[3])//2 ] for bb,_ in detections])
        if len(self.objects)==0:
            for i in range(len(input_centroids)):
                self.register(input_centroids[i])
        else:
            # simple greedy assignment
            objectIDs = list(self.objects.keys())
            object_centroids = list(self.objects.values())
            D = np.linalg.norm(np.array(object_centroids)[:,None]-input_centroids, axis=2)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]
            used_cols=set()
            for row,col in zip(rows,cols):
                if col in used_cols: continue
                oid = objectIDs[row]
                self.objects[oid] = input_centroids[col]
                self.disappeared[oid]=0
                used_cols.add(col)
            unused_cols = set(range(len(input_centroids))) - used_cols
            for col in unused_cols:
                self.register(input_centroids[col])
            for oid in list(self.disappeared.keys()):
                self.disappeared[oid]+=1
                if self.disappeared[oid]>self.max_disappeared:
                    self.deregister(oid)
        return self.objects
