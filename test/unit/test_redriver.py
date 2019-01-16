import pytest
import redriver
from mock import call

@pytest.fixture
def mock_sqs_helper(mocker):
    mocker.patch.object(redriver, 'sqs_helper')
    return redriver.sqs_helper


def test_missing_dlq_url():
    with pytest.raises(ValueError):
        redriver.redrive({'MaxMessageCount': 10}, None)


def test_missing_max_message_count():
    with pytest.raises(ValueError):
        redriver.redrive({'DLQUrl': 'mydlq'}, None)


def test_max_message_count_not_integer():
    with pytest.raises(ValueError):
        redriver.redrive({'DLQUrl': 'mydlq', 'MaxMessageCount': 'string'}, None)


def test_max_message_count_negative_integer():
    with pytest.raises(ValueError):
        redriver.redrive({'DLQUrl': 'mydlq', 'MaxMessageCount': -1}, None)


def test_redrive_no_message(mock_sqs_helper):
    mock_sqs_helper.receive_messages.return_value = []
    dlq_url = 'mydlq'
    max_message_count = 10
    redriver.redrive({'DLQUrl': dlq_url, 'MaxMessageCount': max_message_count}, None)

    mock_sqs_helper.get_source_queues.assert_called_once_with(dlq_url)
    mock_sqs_helper.receive_messages.assert_called_once_with(dlq_url, max_message_count)
    mock_sqs_helper.send_messages.assert_not_called()
    mock_sqs_helper.delete_messages.assert_not_called()


def test_redrive(mock_sqs_helper):
    dlq_url = 'mydlq'
    max_message_count = 10
    source_queue = 'mySource'
    mock_sqs_helper.get_source_queues.return_value = [source_queue]
    mock_sqs_helper.receive_messages.side_effect = [[{
        'MessageId': 'myId',
        'Body': 'This is my message',
        'MessageAttributes': [],
        'ReceiptHandle': 'myHandle'
    }], []]
    redriver.redrive({'DLQUrl': dlq_url, 'MaxMessageCount': max_message_count}, None)

    mock_sqs_helper.get_source_queues.assert_called_once_with(dlq_url)
    mock_sqs_helper.receive_messages.assert_has_calls([call(dlq_url, max_message_count), call(dlq_url, max_message_count - 1)])
    mock_sqs_helper.send_messages.assert_called_once_with(source_queue, [{
        'Id': 'myId',
        'MessageBody': 'This is my message',
        'MessageAttributes': []
    }])
    mock_sqs_helper.delete_messages.assert_called_once_with(dlq_url, [{
        'Id': 'myId',
        'ReceiptHandle': 'myHandle'
    }])


