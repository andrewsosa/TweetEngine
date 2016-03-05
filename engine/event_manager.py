from numpy import diff

import datetime

def safe_get(l, idx, default):
  try:
    return l[idx]
  except IndexError:
    return default

class EventManager():

    def __init__(self):
        self.base = []
        self.last = datetime.datetime.now()

    def record(self, measure):

        # Record
        self.base.append(float(measure))

        # How long has it been?
        period = (datetime.datetime.now() - self.last).total_seconds()
        self.last = datetime.datetime.now()

        # Find out deltas
        d1 = diff(self.base)/period
        d2 = diff(d1)/period

        # Cleanup
        if len(self.base) > 10:
            self.base.pop(0)

        return float('%.3f'%(safe_get(d1, -1, 0))), float('%.3f'%(safe_get(d2, -1, 0)))
