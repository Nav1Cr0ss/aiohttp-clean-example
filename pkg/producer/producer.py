from abc import ABC, abstractmethod

from pkg.producer.dto.message import MsgPayload


class ProducerIface(ABC):
    @abstractmethod
    async def send(self, value: MsgPayload) -> bool:
        ...
