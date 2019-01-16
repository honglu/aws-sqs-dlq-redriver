"""Lambda function handler."""

# must be the first import in files with lambda function handlers
import lambdainit  # noqa: F401

import lambdalogging
import sqs_helper

LOG = lambdalogging.getLogger(__name__)
RECEIVE_MESSAGE_MAX_NUMBER_OF_MESSAGES_LIMIT = 10
DLQ_URL_PROPERTY = 'DLQUrl'
MAX_MESSAGE_COUNT_PROPERTY = 'MaxMessageCount'


def redrive(event, context):
    """Lambda function handler."""
    LOG.info('Received event: %s', event)
    _validate(event)
    dlq = event[DLQ_URL_PROPERTY]
    max_message_count = event[MAX_MESSAGE_COUNT_PROPERTY]
    source_queues = sqs_helper.get_source_queues(dlq)
    processed_message_count = 0

    while processed_message_count < max_message_count:
        remaining_message_count = max_message_count - processed_message_count
        messages = sqs_helper.receive_messages(dlq, remaining_message_count)
        LOG.info("Polled %d messages", len(messages))

        if not messages:
            break
        _redrive_messages(dlq, source_queues, messages)
        processed_message_count += len(messages)

    return {'ProcessedMessageCount': processed_message_count}


def _validate(event):
    if DLQ_URL_PROPERTY not in event:
        raise ValueError('{} is missing from event'.format(DLQ_URL_PROPERTY))
    if MAX_MESSAGE_COUNT_PROPERTY not in event:
        raise ValueError('{} is missing from event'.format(MAX_MESSAGE_COUNT_PROPERTY))
    try:
        max_message_count = int(event[MAX_MESSAGE_COUNT_PROPERTY])
        if max_message_count <= 0:
            raise ValueError('{} must be greater than 0'.format(MAX_MESSAGE_COUNT_PROPERTY))
    except ValueError:
        raise ValueError('{} must be an integer'.format(MAX_MESSAGE_COUNT_PROPERTY))


def _redrive_messages(dlq, source_queues, messages):
    send_message_entries = []
    delete_message_entries = []
    for message in messages:
        send_message_entries.append({
            'Id': message['MessageId'],
            'MessageBody': message['Body'],
            'MessageAttributes': message['MessageAttributes']
        })
        delete_message_entries.append({
            'Id': message['MessageId'],
            'ReceiptHandle': message['ReceiptHandle']
        })
    for source_queue in source_queues:
        sqs_helper.send_messages(source_queue, send_message_entries)

    sqs_helper.delete_messages(dlq, delete_message_entries)
