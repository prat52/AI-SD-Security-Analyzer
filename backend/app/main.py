from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.analyze import router as analyze_router
from app.database.database import engine
from app.models import user, architecture
from app.routes import architecture_routes, auth_routes

app = FastAPI(title="AI Security Architecture Analyzer")

# ✅ CORS must be FIRST before everything
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # ← explicit, not *
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AI Security Architecture Analyzer API Running"}

app.include_router(analyze_router, prefix="/api")
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(architecture_routes.router, tags=["Architecture"])

user.Base.metadata.create_all(bind=engine)
architecture.Base.metadata.create_all(bind=engine)