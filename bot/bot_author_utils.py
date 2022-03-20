from typing import List, Optional, Tuple

from pyrogram import Client, types

import database.views

from .text_data import ANSWER_MESSAGE


async def get_msg_to_forward(
    client: Client, chat_id: str, message_id: str
) -> Optional[types.Message]:
    with client:
        msg = await client.get_messages(
            chat_id=chat_id, message_ids=message_id
        )  # TODO: if delete
    return msg


async def get_messages(
    chat_id: str, user_id: str, client: Client
) -> List[Tuple[Optional[types.Message], str]]:
    messages = database.views.get_messages(chat_id, user_id)
    result = []
    for message in messages:
        msg_to_forward = await get_msg_to_forward(
            client, message[3], message[4]
        )
        text_to_send = ANSWER_MESSAGE.format(message[2], message[0])
        result.append((msg_to_forward, text_to_send))
    return result
