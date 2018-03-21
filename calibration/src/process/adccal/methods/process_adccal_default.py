import sys
import numpy as np
import os

try:
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
except:
    CURRENT_DIR = os.path.dirname(os.path.realpath('__file__'))

BASE_PATH = os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(CURRENT_DIR)
                    )
                )
            )
SRC_PATH = os.path.join(BASE_PATH, "src")
PROCESS_PATH = os.path.join(SRC_PATH, "process")
ADCCAL_PATH = os.path.join(PROCESS_PATH, "adccal")

if ADCCAL_PATH not in sys.path:
    sys.path.insert(0, ADCCAL_PATH)

from process_adccal_base import ProcessAdccalBase

class Process(ProcessAdccalBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _initiate(self):
        shapes = {
            "offset": (self._n_rows, self._n_adcs)
        }

        self._result = {
            # must have entries for correction
            "sample_coarse_offset": {
                "data": np.empty(shapes["offset"]),
                "path": "sample/coarse/offset",
                "type": np.int16
            },
            # additional information
            "stddev": {
                "data": np.empty(shapes["offset"]),
                "path": "stddev",
                "type": np.int16
            },
        }

    def _calculate(self):
        print("Start loading data from {} ...".format(self._in_fname), end="")
        data = self._load_data(self._in_fname)
        print("Done.")

        print("Start computing means and standard deviations ...", end="")
        offset = np.mean(data["sample_coarse"], axis=3).astype(np.int)
        self._result["sample_coarse_offset"]["data"] = offset

        self._result["stddev"]["data"] = data["sample_coarse"].std(axis=3)
        print("Done.")
