"""SQS Helper."""

import lambdalogging
import boto3

LOG = lambdalogging.getLogger(__name__)
SQS = boto3.client('sqs')
RECEIVE_MESSAGE_MAX_NUMBER_OF_MESSAGES_LIMIT = 10


def receive_messages(queue_url, max_message):
    """
    Receive messages from SQS queue.

    :param queue_url: the URL of the SQS queue
    :param max_message: maximum number of messages to receive
    :return: received messages list
    """
    LOG.info('Receiving messages from queue %s', queue_url)
    receive_message_count = min(max_message, RECEIVE_MESSAGE_MAX_NUMBER_OF_MESSAGES_LIMIT)
    return SQS.receive_message(QueueUrl=queue_url,
                               MaxNumberOfMessages=receive_message_count,
                               MessageAttributeNames=['All'])['Messages']


def get_source_queues(queue_url):
    """
    Get the source queues of an SQS DLQ.

    :param queue_url: SQS DLQ URL
    :return: a list of SQS queues
    """
    LOG.info('Getting source queues from queue %s', queue_url)
    return SQS.list_dead_letter_source_queues(QueueUrl=queue_url)['queueUrls']


def send_messages(queue_url, messages):
    """
    Send messages to an SQS queue.

    :param queue_url: SQS queue URL
    :param messages: messages to send to the SQS queue
    """
    LOG.info('Sending messages to queue %s', queue_url)
    send_message_response = SQS.send_message_batch(QueueUrl=queue_url, Entries=messages)
    if 'Failed' in send_message_response:
        raise Exception('Failed to send messages to queue {}. Failed messages: {}'
                        .format(queue_url, send_message_response['Failed']))


def delete_messages(queue_url, messages):
    """
    Delete messages from an SQS queue.

    :param queue_url: SQS queue URL
    :param messages: message to delete from the SQS queue
    """
    LOG.info('Deleting messages from queue %s', queue_url)
    delete_message_response = SQS.delete_message_batch(QueueUrl=queue_url, Entries=messages)
    if 'Failed' in delete_message_response:
        raise Exception(
            'Failed to delete messages from queue {}. Failed messages: {}'
            .format(queue_url, delete_message_response['Failed']))
