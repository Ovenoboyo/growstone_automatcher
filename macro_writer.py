import json

import numpy as np
from random import randint

screenWidth = 1080
screenHeight = 1920

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
      
def get_bs_coords(coord, x = True):
  return (coord / (screenWidth if x else screenHeight)) * 100


obj = None
def write_macro(command, x0, y0, x1, y1, steps):
  global obj
  
  if obj is None:
    obj = {
        "Acceleration": 1,
        "CreationTime": "20221105T191229",
        "DoNotShowWindowOnFinish": False,
        "Events": [],
        "LoopDuration": 0,
        "LoopInterval": 0,
        "LoopIterations": 1,
        "LoopType": "TillLoopNumber",
        "MacroSchemaVersion": 3,
        "MergeConfigurations": [
        ],
        "RestartPlayer": False,
        "RestartPlayerAfterMinutes": 60,
        "Shortcut": "Pause"
    }
    
  if len(obj["Events"]) > 0:
    timestamp = obj["Events"][-1]["Timestamp"]
  else:
    timestamp = 0
    
  if command == 'swipe':
      timestamp += 700
      obj['Events'].append({
          "Delta": 0,
          "EventType": "MouseDown",
          "Timestamp": timestamp,
          "X": get_bs_coords(x0, True),
          "Y": get_bs_coords(y0, False)
      })

      for i in range(steps):
          timestamp += randint(20, 30)
          obj["Events"].append({
              "Delta": 0,
              "EventType": "MouseMove",
              "Timestamp": timestamp,
              "X": get_bs_coords(x0 + ((x1 - x0) / steps) * (i + 1), True),
              "Y": get_bs_coords(y0 + ((y1 - y0) / steps) * (i + 1), False)
          },)

      obj["Events"].append({
          "Delta": 0,
          "EventType": "MouseUp",
          "Timestamp": timestamp + 10,
          "X": get_bs_coords(x1, True),
          "Y": get_bs_coords(y1, False)
      })
    
def dump_objs():
  global obj
  
  if obj and len(obj["Events"]) > 0:
    final_timestamp = obj["Events"][-1]["Timestamp"]
  else:
    final_timestamp = 0
  
  out_file = open("C:\\ProgramData\\BlueStacks_nxt\\Engine\\UserData\\InputMapper\\UserScripts\\auto_combine.json", "w")
  json.dump(obj, out_file, cls=NpEncoder, indent=4)
  obj = None
  return final_timestamp
