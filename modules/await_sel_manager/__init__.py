from khl import Bot, Event, Message, EventTypes, Event
from khl.card import Card, CardMessage, Module, Types, Element, Struct
from khl.api import Message as MessageAPI
from loguru import logger

class AwaitingUserSelection:
    def __init__(self):
        self.awaiting_user_selection = dict()

    def add(self, msg_id, callbacks: dict):
        self.awaiting_user_selection[msg_id] = callbacks

    def callback(self, event: Event):
        msg_id = event.body["msg_id"]
        choice = event.body["value"]
        if not msg_id in self.awaiting_user_selection:
            return
        callbacks = self.awaiting_user_selection[msg_id]
        rets = None
        if choice in callbacks:
            try:
                rets = callbacks[choice](event)
            except Exception as e:
                logger.error(f"Error while executing callback {callbacks[choice]} from choice {choice}: {e}")
        else:
            logger.warning(f"Choice {choice} not found in {callbacks}")
        del self.awaiting_user_selection[msg_id]
        return rets
    
    def cancel(self, msg_id):
        if msg_id in self.awaiting_user_selection:
            del self.awaiting_user_selection[msg_id]
        else:
            logger.warning(f"Message {msg_id} not found in awaiting_user_selection")

    def contains(self, msg_id) -> bool:
        return msg_id in self.awaiting_user_selection

await_selection_manager = AwaitingUserSelection()
