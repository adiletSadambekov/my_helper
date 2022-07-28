from datetime import datetime
import asyncio

from utills.generate_images import generate_for_items
from parser.parser import ItemsParse


async def auto_generate_image(point_of_send: datetime) -> None:
    first_started = True
    one_turn = 86220
    while True:
        if first_started:
            now = datetime.now()
            intervals_result = now - point_of_send
            first_started = False
            print('Worked first' + str(intervals_result.seconds))
            close_turn = (one_turn + 180) - intervals_result.seconds
            await asyncio.sleep(close_turn)
        else:
            text = ItemsParse().get_items_times()
            generate_for_items(1, '\n\n'.join(text))
            print('worked two')
            await asyncio.sleep(one_turn)


