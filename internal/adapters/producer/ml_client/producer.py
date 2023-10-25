from pkg.producer.kafka.producer import KafkaProducer


class MlProducer(KafkaProducer):
    def __init__(self, bootstrap_servers):
        super().__init__(
            bootstrap_servers=bootstrap_servers,
            topic="drawing_process")
