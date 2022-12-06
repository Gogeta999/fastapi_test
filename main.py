from fastapi import FastAPI,  APIRouter
from routers import rc_routes, datacenter
from fastapi.responses import RedirectResponse


app = APIRouter()
app = FastAPI(title="Ash999")
app.include_router(rc_routes.router)
app.include_router(datacenter.router)


@app.get("/")
def get_home():
    redirect_url = '/docs' 
    return RedirectResponse(redirect_url)



    
    