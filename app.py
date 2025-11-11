from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import uvicorn

app = FastAPI()

# Setup directories with absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
templates_dir = os.path.join(current_dir, "templates")

print(f"Current directory: {current_dir}")
print(f"Static directory: {static_dir}")
print(f"Templates directory: {templates_dir}")
print(f"Static exists: {os.path.exists(static_dir)}")
print(f"Templates exists: {os.path.exists(templates_dir)}")

# Create directories if they don't exist
os.makedirs(static_dir, exist_ok=True)
os.makedirs(templates_dir, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Main page with the form"""
    return templates.TemplateResponse("vehicledata.html", {"request": request, "context": "Rendering"})

@app.get("/debug-static")
async def debug_static():
    """Debug endpoint to check static files"""
    return JSONResponse({
        "current_directory": current_dir,
        "static_directory": static_dir,
        "templates_directory": templates_dir,
        "static_exists": os.path.exists(static_dir),
        "templates_exists": os.path.exists(templates_dir),
        "static_files": os.listdir(static_dir) if os.path.exists(static_dir) else [],
        "template_files": os.listdir(templates_dir) if os.path.exists(templates_dir) else []
    })

@app.post("/", response_class=HTMLResponse)
async def make_prediction(request: Request):
    """Handle form submission"""
    form_data = await request.form()
    
    # For now, return a simple prediction
    return templates.TemplateResponse("vehicledata.html", {
        "request": request, 
        "context": "Response-Yes",
        "form_data": dict(form_data)
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)