import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class MsgPayload:
    msg: Optional[dict] = None
    payload: Optional[dict] = None

    def to_json(self) -> str:
        data_dict = {}
        if self.msg:
            data_dict["msg"] = self.msg

        if self.payload:
            data_dict["payload"] = self.payload

        return json.dumps(data_dict)
