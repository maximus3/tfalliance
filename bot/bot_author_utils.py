import logging
from typing import List, Tuple

import pyrogram.errors
from pyrogram import Client, types

import database.views

from .text_data import ANSWER_MESSAGE, MSG_BY_AUTHOR

logger = logging.getLogger(__name__)


async def get_messages(
    chat_id: str, user_id: str
) -> List[Tuple[Tuple[str, int], str]]:
    messages = database.views.get_messages(chat_id, user_id)
    result = []
    for message in messages:
        msg_to_forward_data = (message[3], int(message[4]))
        text_to_send = ANSWER_MESSAGE.format(message[2], message[0])
        result.append((msg_to_forward_data, text_to_send))
    return result


async def reply_message(client: Client, message: types.Message) -> bool:
    sender_id = str(message.reply_to_message.forward_from.id)
    text = message.reply_to_message.text

    chat_id, reply_to_message_id = database.views.get_chat_message_ids(
        str(message.chat.id), str(message.from_user.id), sender_id, text
    )
    if chat_id is None:
        logger.exception('Error in get_chat_message_ids')
        return False

    try:
        if reply_to_message_id is not None:
            await client.send_message(
                chat_id,
                MSG_BY_AUTHOR.format(message.text),
                reply_to_message_id=int(reply_to_message_id),
            )
        else:
            await client.send_message(
                chat_id, MSG_BY_AUTHOR.format(message.text)
            )
    except pyrogram.errors.exceptions.bad_request_400.PeerIdInvalid:
        logger.exception('Error in send_message to user 400')
        return False
    return True
