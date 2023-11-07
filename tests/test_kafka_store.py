from unittest import TestCase

from mockafka.kafka_store import KafkaStore, KafkaException, Message


class TestKafkaStore(TestCase):
    TEST_TOPIC = 'test_topic'
    DEFAULT_PARTITION = 16
    DEFAULT_MESSAGE = Message(
        headers=None,
        key='test_key',
        value='{"test_value": "ok"}',
        topic=TEST_TOPIC,
        offset=None,
        error=None,
        latency=None,
        leader_epoch=None,
        partition=0,
        timestamp=None,
    )

    def setUp(self) -> None:
        self.kafka = KafkaStore(clean=True)

    def _create_topic_partition(self):
        self.kafka.create_topic(topic=self.TEST_TOPIC)
        self.kafka.create_partition(topic=self.TEST_TOPIC, partitions=self.DEFAULT_PARTITION)

    def test_is_topic_exist(self):
        # check topic not exist
        self.assertFalse(self.kafka.is_topic_exist(topic=self.TEST_TOPIC))

        self.kafka.create_topic(topic=self.TEST_TOPIC)

        # check topic exist
        self.assertTrue(self.kafka.is_topic_exist(self.TEST_TOPIC))

    def test_is_partition_exist_on_topic(self):
        # create topic and partition
        self._create_topic_partition()

        # test partition exist
        self.assertTrue(self.kafka.is_partition_exist_on_topic(topic=self.TEST_TOPIC, partition_num=11))
        self.assertTrue(self.kafka.is_partition_exist_on_topic(topic=self.TEST_TOPIC, partition_num=0))
        self.assertTrue(self.kafka.is_partition_exist_on_topic(topic=self.TEST_TOPIC, partition_num=15))

        # test partition not exist
        self.assertFalse(self.kafka.is_partition_exist_on_topic(topic=self.TEST_TOPIC, partition_num=16))

    def test_get_number_of_partition(self):
        self._create_topic_partition()

        self.assertEqual(self.kafka.get_number_of_partition(topic=self.TEST_TOPIC), self.DEFAULT_PARTITION)

    def test_create_topic(self):
        self.kafka.create_topic(topic=self.TEST_TOPIC)

        self.assertTrue(self.kafka.is_topic_exist(self.TEST_TOPIC))

    def test_create_topic_that_exist(self):
        self.kafka.create_topic(topic=self.TEST_TOPIC)

        # test exception when topic exist
        with self.assertRaises(KafkaException):
            self.kafka.create_topic(topic=self.TEST_TOPIC)

    def test_remove_topic(self):
        # test partition not exist
        self.kafka.remove_topic(topic=self.TEST_TOPIC)

        # create topic
        self.kafka.create_topic(topic=self.TEST_TOPIC)
        self.kafka.remove_topic(topic=self.TEST_TOPIC)

        self.assertFalse(self.kafka.is_topic_exist(topic=self.TEST_TOPIC))

    def test_set_first_offset(self):
        pass

    def test__add_next_offset(self):
        pass

    def test_get_offset_store_key(self):
        pass

    def test_produce(self):
        self._create_topic_partition()

        self.assertEqual(
            self.kafka.get_messages_in_partition(topic=self.TEST_TOPIC, partition=0), []
        )

        # test produce on partition 0
        self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=0)

        self.assertEqual(
            self.kafka.get_messages_in_partition(topic=self.TEST_TOPIC, partition=0), [self.DEFAULT_MESSAGE]
        )

        # test produce on partition 1
        self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=1)
        self.assertEqual(
            self.kafka.get_messages_in_partition(topic=self.TEST_TOPIC, partition=1), [self.DEFAULT_MESSAGE]
        )

    def test_get_message(self):
        self._create_topic_partition()

        self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=1)
        self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=1)
        self.assertEqual(
            self.kafka.get_message(topic=self.TEST_TOPIC, partition=1, offset=0), self.DEFAULT_MESSAGE
        )
        self.assertEqual(
            self.kafka.get_message(topic=self.TEST_TOPIC, partition=1, offset=1), self.DEFAULT_MESSAGE
        )

    def test_get_partition_first_offset(self):
        pass

    def test_get_partition_next_offset(self):
        pass

    def test_topic_list(self):
        # test empty topic
        self.assertEqual(self.kafka.topic_list(), [])

        topics_to_add = [self.TEST_TOPIC, self.TEST_TOPIC + '01', self.TEST_TOPIC + '02']
        for topic in topics_to_add:
            self.kafka.create_topic(topic=topic)

        self.assertEqual(self.kafka.topic_list(), topics_to_add)

    def test_partition_list(self):
        self._create_topic_partition()

        self.assertEqual(self.kafka.partition_list(topic=self.TEST_TOPIC), list(range(0, self.DEFAULT_PARTITION)))

        self.kafka.create_partition(topic=self.TEST_TOPIC, partitions=self.DEFAULT_PARTITION + 16)
        self.assertEqual(self.kafka.partition_list(topic=self.TEST_TOPIC), list(range(0, self.DEFAULT_PARTITION + 16)))

    def test_get_messages_in_partition(self):
        pass

    def test_number_of_message_in_topic(self):
        pass

    def test_clear_topic_messages(self):
        pass

    def test_clear_partition_messages(self):
        pass

    def test_reset_offset(self):
        pass
