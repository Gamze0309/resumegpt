SECTION_KEYWORDS = ["profile", "professional experience", "experience", "education", "skills", "projects", "certifications", "summary", "contact", "languages", "awards", "strenghts", "courses", "tools"]

def detect_sections(text):
    lines = text.splitlines()
    sections = {}
    current_section = "other"
    sections[current_section] = []

    for line in lines:
        stripped = line.strip().lower()
        
        if stripped in SECTION_KEYWORDS:
            print(stripped)
            current_section = stripped
            sections[current_section] = []
        else:
            sections[current_section].append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items() if v}
