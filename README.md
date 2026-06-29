# PDF/Image to LaTeX Converter

> **Convert PDFs and scanned images (JPG/PNG) to ready-to-compile LaTeX code** using Mistral OCR and custom templates.

This application implements the complete workflow from the pdf-image-to-latex skill, with systematic image extraction, formula detection, and proper LaTeX formatting.

## Features

- Multi-format support: PDF, JPG, PNG
- Automatic OCR: Powered by Mistral OCR API
- Template system: Standard, Physics, Chemistry templates
- Formula detection: Math, chemistry, and physics formulas
- Unit conversion: Automatic \SI{}{}{} formatting
- Image extraction: ALL images extracted and referenced
- Exercise formatting: Automatic \exo{n} conversion
- Preview & download: See first 50 lines, download ZIP

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Mistral OCR API key (Pro account)

### Installation
```bash
# Clone the repository
git clone https://github.com/yannslivecode/pdf-to-latex-app.git
cd pdf-to-latex-app

# Copy environment file
cp .env.example .env

# Edit .env and add your Mistral API key
nano .env

# Start the application
docker-compose up --build
```

### Access
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure
```
pdf-to-latex-app/
├── README.md
├── LICENSE
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker/
│   └── nginx.conf
├── backend/
│   ├── __init__.py
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── ocr.py
│       │   ├── postprocessing.py
│       │   ├── templates.py
│       │   └── utils.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── schemas.py
│       └── routes/
│           ├── __init__.py
│           ├── conversion.py
│           └── files.py
│       └── static/
│           ├── templates/
│           │   ├── standard.tex
│           │   ├── physics.tex
│           │   └── chemistry.tex
│           └── cours_FARNIER.txt
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    ├── tsconfig.node.json
    └── src/
        ├── main.tsx
        ├── index.css
        ├── App.tsx
        ├── types/
        │   └── index.ts
        └── services/
            └── api.ts
```

## Usage

### Web Interface
1. Upload PDF/JPG/PNG
2. Select template (standard/physics/chemistry)
3. Click "Convert to LaTeX"
4. Download ZIP with output.tex + images

### API
```bash
# Convert file
curl -X POST http://localhost:8000/api/convert \
  -F 'file=@document.pdf' \
  -F 'template=physics'

# Download result
curl -OJ http://localhost:8000/api/download/TASK_ID
```

## Configuration
Edit .env:
```bash
MISTRAL_API_KEY=your_api_key_here
OCR_MODEL=mistral-ocr-latest
OCR_LANGUAGE=fr
```

## Workflow Details

The application follows the 5-phase workflow from the pdf-image-to-latex skill:

### Phase 1: Input Analysis
- Accepts PDF, JPG, or PNG files
- Detects document type (math, physics, chemistry, mixed)
- Allows template selection

### Phase 2: Mistral OCR Extraction
- Calls Mistral OCR API with extract_images: true
- Returns text, images, and metadata

### Phase 3: Post-Processing
- Math formulas: v→ → \V{v}, d/dt → \derd{}{t}
- Units: 9.81 m/s² → \SI{9.81}{\meter\per\second\squared}
- Exercises: Exercice 12 → \exo{12}
- Images: All extracted and referenced

### Phase 4: Template Application
- Merges content with selected template
- Ensures mandatory preamble is present

### Phase 5: Output & Storage
- Generates output.tex
- Saves extracted images to /images/
- Creates ZIP archive for download

## License
MIT License
