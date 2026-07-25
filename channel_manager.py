from telegram_client import get_client


async def get_channels():

    client = get_client()

    result = []

    dialogs = await client.get_dialogs()

    for dialog in dialogs:

        entity = dialog.entity

        if getattr(entity, "broadcast", False):

            result.append(
                {
                    "title": entity.title,
                    "id": entity.id
                }
            )

    return result