from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.health import router as health_router
from app.routes.skills import router as skills_router
from app.routes.roles import router as roles_router
from app.routes.companies import router as companies_router
from app.routes.graph import router as graph_router

app = FastAPI(
    title="CareerGraph API",
    description="Graph-powered career exploration platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://career-graph-tau.vercel.app",
        "http://localhost:5173",
        "http://localhost:4173",
    ],
    allow_origin_regex=r"https://career-graph-[a-z0-9-]+\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(skills_router)
app.include_router(roles_router)
app.include_router(companies_router)
app.include_router(graph_router)


@app.get("/")
def root():
    return {
        "message": "CareerGraph API is running"
    }