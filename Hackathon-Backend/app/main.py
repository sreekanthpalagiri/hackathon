from fastapi import FastAPI, Request, Form  
from fastapi.responses import HTMLResponse, JSONResponse  
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse  
#from fastapi.middleware.cors import CORSMiddleware
from queue import Queue  
import asyncio  
 
app = FastAPI()  
'''
# Allow frontend access  
app.add_middleware(  
    CORSMiddleware,  
    allow_origins=["*"],  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)
'''
 
# Mount static files directory (for CSS and JS)  
app.mount("/static", StaticFiles(directory="static"), name="static")
 
# Queue to store bot responses  
bot_responses = Queue()  
 
@app.get("/", response_class=HTMLResponse)  
async def get_chat_page():  
    with open("index.html") as f:  
        html_content = f.read()  
    return HTMLResponse(content=html_content)  
 
@app.post("/send-message")  
async def send_message(request: Request):  
    data = await request.json()  
    user_message = data.get("message")  
    print(f"Received User Message: {user_message}")
     
    # Simulate a bot response  
    bot_responses.put(f"Bot: You said '{user_message}'")  
    return JSONResponse(content={"status": "success"})  
 
@app.get("/chat-stream")  
async def chat_stream():  
    async def event_generator():  
        while True:  
            if not bot_responses.empty():  
                yield bot_responses.get()  
            await asyncio.sleep(0.1)  
    return EventSourceResponse(event_generator())  
 
### REMOVE THIS IN PROD
### Add test messages to bot_responses ...
@app.post("/add-test-message")  
async def add_test_message(request: Request):  
    data = await request.json()  
    test_message = data.get("message")  
    print(f"Received Test Message: {test_message}")
 
    # Add the test message to the bot_responses queue  
    bot_responses.put(f"Bot (Test): {test_message}")  
    return JSONResponse(content={"status": "test message added"})
### REMOVE THIS IN PROD
 
'''
curl -X POST http://127.0.0.1:8000/add-test-message -H "Content-Type: application/json" -d '{"message": "Hello from the test route!"}'  
'''
 
if __name__ == "__main__":  
    import uvicorn  
    uvicorn.run(app, host="127.0.0.1", port=8000)