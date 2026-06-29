from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import conversion, files

app = FastAPI(
    title="PDF/Image to LaTeX Converter API",
    description="Convert PDFs and images to ready-to-compile LaTeX code using Mistral OCR",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conversion.router, prefix="/api", tags=["conversion"])
app.include_router(files.router, prefix="/api", tags=["files"])


@app.get("/")
def root():
    return {"message": "PDF/Image to LaTeX Converter API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}