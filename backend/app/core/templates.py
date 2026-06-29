import re
from pathlib import Path
from app.core.config import settings

MANDATORY_PREAMBLE = r"""\documentclass[french,a4paper]{article}

\usepackage{cours_FARNIER}

\excludeversion{notecours}
%\includeversion{notecours}
\newenvironment{note}{\notecours \itshape }{\endnotecours}

\begin{document}
"""

def get_template_path(template_name: str) -> Path:
    return Path(settings.TEMPLATES_DIR) / f"{template_name}.tex"

def load_template(template_name: str) -> str:
    template_path = get_template_path(template_name)
    if not template_path.exists():
        return MANDATORY_PREAMBLE + "\n%% CONTENT %%\n\end{document}"
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

def apply_template(content: str, template_name: str) -> str:
    template = load_template(template_name)
    
    if "%% CONTENT %%" in template:
        final = template.replace("%% CONTENT %%, content)
    elif "%===== CONTENT START =====" in template:
        parts = template.split("%===== CONTENT START =====")
        if len(parts) > 1:
            after_parts = parts[1].split("%===== CONTENT END =====")
            final = f"{parts[0]}{content}{after_parts[1] if len(after_parts) > 1 else ''}"
        else:
            final = template + content
    else:
        final = template + content
    
    if MANDATORY_PREAMBLE not in final:
        final = re.sub(r'\\documentclass.*?\n', '', final, flags=re.DOTALL)
        final = MANDATORY_PREAMBLE + final
    
    return final
