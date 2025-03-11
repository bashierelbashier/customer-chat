from fastapi import WebSocket


class Chat():

    def __init__(self, customer_ws: WebSocket = None, support_ws: WebSocket = None):
        self.customer_ws = customer_ws
        self.support_ws = support_ws
        self.PENDING_MESSAGES = []

    def assign_support_ws(self, support_ws: WebSocket):
        self.support_ws = support_ws

    async def send_pending_messages(self):
        while self.PENDING_MESSAGES:
            await self.send_to_support(self.PENDING_MESSAGES.pop())
    
    async def send_to_customer(self, message):
        await self.customer_ws.send_text(f"Support: {message}")

    async def send_to_support(self, message):
        await self.support_ws.send_text(f"Customer: {message}")
