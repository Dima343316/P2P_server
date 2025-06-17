from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()
node_ref = None

@app.get("/peers")
def get_peers():
    if not node_ref:
        return {"peers": []}
    return {"peers": [f"{c.getpeername()[0]}:{c.getpeername()[1]}" for c in node_ref.peers]}

@app.post("/relay")
async def relay(request: Request):
    data = await request.json()
    msg = data.get("message", "")
    print(f"[HTTP] Relaying message: {msg}")  # Должно выводиться
    if node_ref:
        node_ref.broadcast(msg)
    return {"status": "ok", "message": msg}

def start_http_server(node, port=8000):
    global node_ref
    node_ref = node
    uvicorn.run(app, host="0.0.0.0", port=port)
