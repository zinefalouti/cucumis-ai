from fastapi import FastAPI, Query, HTTPException
from model import scanImg, FetchModel  
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import File, UploadFile
from fastapi.responses import StreamingResponse
import io
from PIL import Image
import cv2
import numpy

app = FastAPI()


# Mount static files folder (optional)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates folder
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#Upload
@app.post("/upload")
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")

        model = FetchModel()

        results = model(img)
        result = results[0]         # get first result

        img_with_boxes_bgr = result.plot()  # BGR format by default
        img_with_boxes_rgb = cv2.cvtColor(img_with_boxes_bgr, cv2.COLOR_BGR2RGB)  # convert to RGB

        img_pil = Image.fromarray(img_with_boxes_rgb)

        buf = io.BytesIO()
        img_pil.save(buf, format="PNG")
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#Scan
@app.get("/scan")
def read_item(imgurl: str = Query(..., description="URL of the image to scan")):
    try:
        result = scanImg(imgurl)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))