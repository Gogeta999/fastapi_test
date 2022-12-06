from fastapi import FastAPI,  APIRouter
from routers import rc_routes, datacenter
from fastapi.responses import RedirectResponse


router = APIRouter()
router = FastAPI(title="Ash999")
router.include_router(rc_routes.router)
router.include_router(datacenter.router)

@router.get("/")
def get_home():
    redirect_url = '/docs' 
    return RedirectResponse(redirect_url)




    
    