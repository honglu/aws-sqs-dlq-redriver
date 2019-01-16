import pytest
import sqs_helper


@pytest.fixture
def mock_sqs(mocker):
    mocker.patch.object(sqs_helper, 'SQS')
    return sqs_helper.SQS


def test_receive_messages(mock_sqs):
    dlq_url = 'mydlq'
    max_message_count = 9
    messages = [{'MessageId': 'myId'}]
    mock_sqs.receive_message.return_value = {'Messages': messages}

    assert sqs_helper.receive_messages(dlq_url, max_message_count) == messages
    mock_sqs.receive_message.assert_called_once_with(QueueUrl=dlq_url, MaxNumberOfMessages=max_message_count)


def test_receive_messages_more_than_default_max_message(mock_sqs):
    dlq_url = 'mydlq'
    max_message_count = 11
    messages = [{'MessageId': 'myId'}]
    mock_sqs.receive_message.return_value = {'Messages': messages}

    assert sqs_helper.receive_messages(dlq_url, max_message_count) == messages
    mock_sqs.receive_message.assert_called_once_with(QueueUrl=dlq_url, MaxNumberOfMessages=10)


def test_get_source_queues(mock_sqs):
    dlq_url = 'mydlq'
    urls = ['myUrl']
    mock_sqs.list_dead_letter_source_queues.return_value = {'queueUrls': urls}

    assert sqs_helper.get_source_queues(dlq_url) == urls
    mock_sqs.list_dead_letter_source_queues.assert_called_once_with(QueueUrl=dlq_url)


def test_send_messages(mock_sqs):
    dlq_url = 'mydlq'
    messages = [{'MessageId': 'myId'}]
    mock_sqs.send_message_batch.return_value = {'Successful': []}

    sqs_helper.send_messages(dlq_url, messages)
    mock_sqs.send_message_batch.assert_called_once_with(QueueUrl=dlq_url, Entries=messages)


def test_send_messages_failed(mock_sqs):
    dlq_url = 'mydlq'
    messages = [{'MessageId': 'myId'}]
    mock_sqs.send_message_batch.return_value = {'Failed': []}

    with pytest.raises(Exception):
        sqs_helper.send_messages(dlq_url, messages)
    mock_sqs.send_message_batch.assert_called_once_with(QueueUrl=dlq_url, Entries=messages)


def test_delete_messages(mock_sqs):
    queue_url = 'myqueue'
    messages = [{'MessageId': 'myId'}]
    mock_sqs.delete_message_batch.return_value = {'Successful': []}

    sqs_helper.delete_messages(queue_url, messages)
    mock_sqs.delete_message_batch.assert_called_once_with(QueueUrl=queue_url, Entries=messages)


def test_delete_messages_failed(mock_sqs):
    queue_url = 'myqueue'
    messages = [{'MessageId': 'myId'}]
    mock_sqs.delete_message_batch.return_value = {'Failed': []}

    with pytest.raises(Exception):
        sqs_helper.delete_messages(queue_url, messages)
    mock_sqs.delete_message_batch.assert_called_once_with(QueueUrl=queue_url, Entries=messages)
