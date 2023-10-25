import asyncio

from aiokafka import AIOKafkaProducer

from pkg.producer.dto.message import MsgPayload
from pkg.producer.producer import ProducerIface


class KafkaProducer(ProducerIface):
    def __init__(self, bootstrap_servers, topic):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = None

    async def _start(self):
        self.producer = AIOKafkaProducer(
            loop=asyncio.get_event_loop(),
            bootstrap_servers=self.bootstrap_servers,
        )
        await self.producer.start()

    async def _stop(self):
        if self.producer:
            await self.producer.stop()

    async def send(self, value: MsgPayload) -> bool:
        # Also it is very confident producer
        if value.msg or value.payload:
            return True

        if not self.producer:
            raise RuntimeError("Kafka producer has not been started.")

        await self.producer.send_and_wait(self.topic, value.to_json())

    async def __aenter__(self):
        await self._start()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._stop()
