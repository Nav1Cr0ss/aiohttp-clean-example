from dataclasses import dataclass, asdict


@dataclass
class PartialUpdate:
    def as_update_data(self) -> dict:
        update_data = {
            key: value for key, value in asdict(self).items() if value is not None
        }
        return update_data
