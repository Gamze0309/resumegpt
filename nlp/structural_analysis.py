import re
import spacy

nlp = spacy.load("en_core_web_sm")

def structural_analysis(parsed_sections):
    result_of_found_sections = get_result_of_found_sections(parsed_sections)
    return result_of_found_sections

def get_result_of_found_sections(parsed_sections):
    mandatory_sections = ["experience", "education", "skills", "contact"]
    recommended_sections = ["projects", "certifications", "languages"]
    missing_sections = []
    missing_recommended_sections = []
    return_texts = []

    section_names = parsed_sections.keys()

    # missing_sections includes missing mandatory sections.
    for required in mandatory_sections:
        if not any(required in section_name for section_name in section_names):
            missing_sections.append(required)

    contact_text = parsed_sections.get("contact")
    
    if contact_text:
        has_contact, contact_validate_text = get_contact_result(contact_text)
    else:
        other_text = parsed_sections.get("other", "")
        has_contact, contact_validate_text = get_contact_result(other_text)
        if has_contact:
            missing_sections.remove("contact")

    return_texts += contact_validate_text

    if len(missing_sections) > 0:
        return_texts.append("Mandatory sections are missing: " + ", ".join(missing_sections) + ".")
    else:
        return_texts.append("You provided mandatory sections.")

    # missing_recommended_sections includes missing recommended sections.
    for recommended in recommended_sections:
        if not any(recommended in section_name for section_name in section_names):
            missing_recommended_sections.append(recommended)

    if len(missing_recommended_sections) > 0:
        return_texts.append("Some recommended sections are missing: " + ", ".join(missing_recommended_sections) + ".")
    else:
        return_texts.append("You provided recommended sections (projects, certifications and languages).")
    
    # Check for the all sections are not blank
    for section, content in parsed_sections.items():
        if not bool(content.strip()):
            return_texts.append(section + " section content are missing.")

    return return_texts

# The contact section may not always appear under the "contact" heading in the resume.
# It can also be labeled as something like "summary".
# Therefore, we need to check for the presence of contact information like an email or phone number.
def get_contact_result(text):
    contact_found = False
    contact_validate_text = []
    
    if has_email(text):
        contact_found = True
        contact_validate_text.append("You provided your email. Recruiters can use your email to contact you for job matches.")
    else:
        contact_validate_text.append("You did not provide your email. Recruiters will not be able to contact you directly for job matches.")

    if has_phone_number(text):
        contact_found = True
        contact_validate_text.append("You provided your phone number. Recruiters can use your phone number to contact you for job matches.")
    else:
        contact_validate_text.append("You did not provide your phone number. Recruiters will not be able to contact you directly for job matches.")

    if has_address(text):
        contact_found = True
        contact_validate_text.append("You provided your address. Recruiters use your address to validate your location for job matches.")
    else:
        contact_validate_text.append("You did not provide your address. Recruiters cannot validate your location for job matches.")
    
    if has_website(text):
        contact_found = True
        contact_validate_text.append("By linking to a website, you've strengthened your web credibility. Recruiters find it helpful and reliable when candidates include a professional site.")
    else:
        contact_validate_text.append("You haven’t linked to a website, which may limit your web credibility. Adding a professional site is recommended, as recruiters often find it helpful and reliable.")

    return contact_found, contact_validate_text

def has_email(other_text):
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    return bool(re.search(email_pattern, other_text))

def has_phone_number(other_text):
    phone_pattern = r'(\+?\d{1,3}[\s\-\.]?)?(\(?\d{2,4}\)?[\s\-\.]?)?[\d\s\-\.]{6,}'
    return bool(re.search(phone_pattern, other_text))

def has_address(text):
    doc = nlp(text)
    return any(ent.label_ == "GPE" for ent in doc.ents)

def has_website(other_text):
    pattern = r"(https?://|www\.)[^\s]+"
    return bool(re.search(pattern, other_text, re.IGNORECASE))