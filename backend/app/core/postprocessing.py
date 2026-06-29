import re
from typing import Tuple, List, Dict

def convert_math_formulas(text: str) -> str:
    text = re.sub(r'(\w)→', r'\\V{\1}', text)
    text = re.sub(r'\bd(\w+)/d(\w+)\b', r'\\derd{\1}{\2}', text)
    text = re.sub(r'\bd²(\w+)/d(\w+)²\b', r'\\derdd{\1}{\2}', text)
    text = re.sub(r'\bd(\w+)/d(\w+)²\b', r'\\derdd{\1}{\2}', text)
    text = re.sub(r'\|([^|]+)\|', r'\\norme{\1}', text)
    return text

def convert_units(text: str) -> str:
    conversions = [
        (r'(\d+\.?\d*)\s*m/s', r'\\SI{\1}{\meter\\per\\second}'),
        (r'(\d+\.?\d*)\s*km/h', r'\\SI{\1}{\kilo\\meter\\per\\hour}'),
        (r'(\d+\.?\d*)\s*m/s²', r'\\SI{\1}{\meter\\per\\second\\squared}'),
        (r'(\d+\.?\d*)\s*N\b', r'\\SI{\1}{\newton}'),
        (r'(\d+\.?\d*)\s*J\b', r'\\SI{\1}{\joule}'),
        (r'(\d+\.?\d*)\s*W\b', r'\\SI{\1}{\watt}'),
        (r'(\d+\.?\d*)\s*C\b', r'\\SI{\1}{\coulomb}'),
    ]
    for pattern, replacement in conversions:
        text = re.sub(pattern, replacement, text)
    return text

def enhance_structure(text: str) -> str:
    text = re.sub(r'\bExercice\s+(\d+)\b', r'\\exo{\1}', text, flags=re.IGNORECASE)
    text = re.sub(r'\bExercise\s+(\d+)\b', r'\\exo{\1}', text, flags=re.IGNORECASE)
    text = re.sub(r'^\s*(Données:|Questions:)\s*$', r'\\subsection*{\1}', text, flags=re.MULTILINE)
    return text

def add_image_references(text: str, images: List[Dict]) -> str:
    if len(images) > 0:
        image_refs = "\n\n".join([
            f"% Image {i+1}: \\includegraphics[{{width=0.5\\linewidth}}]{{images/{img['name']}}}"
            for i, img in enumerate(images)
        ])
        text = f"{text}\n\n{image_refs}"
    return text

def postprocess_content(ocr_result: Dict, template: str) -> Tuple[str, List[str]]:
    warnings = []
    text = ocr_result.get("text", "")
    images = ocr_result.get("images", [])
    
    text = convert_math_formulas(text)
    text = convert_units(text)
    text = enhance_structure(text)
    text = add_image_references(text, images)
    
    if template == "physics":
        for i, img in enumerate(images):
            if "circuit" in img.get("name", "").lower():
                warnings.append(f"REVIEW_NEEDED: Potential circuit diagram (image_{i}.png)")
    
    return text, warnings
