from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .chat import Chat

CHATS = []
app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse(
        request=request, name="customer.html"
    )


@app.get("/support", response_class=HTMLResponse)
async def get_support(request: Request):
    return templates.TemplateResponse(
        request=request, name="support.html"
    )


@app.websocket("/wsc")
async def websocket_endpoint_customer(websocket: WebSocket):
    await websocket.accept()
    CHATS.append(Chat(customer_ws=websocket))
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"You: {data}")
            chat = list(filter(lambda chat: chat.customer_ws == websocket, CHATS))[:1]
            if len(chat) > 0 and chat[0].support_ws:
                chat[0].customer_ws = websocket
                await chat[0].send_to_support(data)
            elif len(chat) > 0:
                chat[0].PENDING_MESSAGES.append(data)
                await chat[0].send_to_customer("An agent will contact you soon!")
    except WebSocketDisconnect:
        chat = list(filter(lambda chat: chat.customer_ws == websocket, CHATS))[:1]
        if len(chat) > 0 and chat[0].support_ws:
            await chat[0].send_to_support("disconnected!")


@app.websocket("/wss")
async def websocket_endpoint_support(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            waiting_chat = list(filter(lambda chat: chat.support_ws == websocket or not chat.support_ws, CHATS))[:1]
            if len(waiting_chat) > 0:
                waiting_chat[0].support_ws = websocket
                await websocket.send_text(f"You: {data}")
                await waiting_chat[0].send_pending_messages()
                await waiting_chat[0].send_to_customer(data)
    except WebSocketDisconnect:
        chat = list(filter(lambda chat: chat.support_ws == websocket, CHATS))[:1]
        if len(chat) > 0 and chat[0].customer_ws:
            await chat[0].send_to_customer("disconnected!")
