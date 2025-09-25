from datetime import datetime
import re
from structural_analysis import nlp

DATE_FORMATS = ["%m/%Y", "%b %Y", "%B %Y", "%Y", "%m-%Y"]
COMPANY_SUFFIXES = ["inc", "llc", "ltd", "corporation", "company", "technologies", "systems", "group", "solutions", "corp", "a.s.", "automation"]

def contextual_analysis(parsed_sections):
    result_of_contact = control_contact(parsed_sections)
    result_of_experience_detail = control_experience_detail(parsed_sections)

def control_contact(parsed_sections):
    contact_text = parsed_sections.get("contact")
    
    if not contact_text:
        contact_text = parsed_sections.get("other", "")
    contact_validate_text = get_contact_result(contact_text)

    return contact_validate_text

# The contact section may not always appear under the "contact" heading in the resume.
# It can also be labeled as something like "summary".
# Therefore, we need to check for the presence of contact information like an email or phone number.
def get_contact_result(text):
    contact_validate_text = []
    
    if has_email(text):
        contact_validate_text.append("You provided your email. Recruiters can use your email to contact you for job matches.")
    else:
        contact_validate_text.append("You did not provide your email. Recruiters will not be able to contact you directly for job matches.")

    if has_phone_number(text):
        contact_validate_text.append("You provided your phone number. Recruiters can use your phone number to contact you for job matches.")
    else:
        contact_validate_text.append("You did not provide your phone number. Recruiters will not be able to contact you directly for job matches.")

    if has_address(text):
        contact_validate_text.append("You provided your address. Recruiters use your address to validate your location for job matches.")
    else:
        contact_validate_text.append("You did not provide your address. Recruiters cannot validate your location for job matches.")
    
    if has_website(text):
        contact_validate_text.append("By linking to a website, you've strengthened your web credibility. Recruiters find it helpful and reliable when candidates include a professional site.")
    else:
        contact_validate_text.append("You haven’t linked to a website, which may limit your web credibility. Adding a professional site is recommended, as recruiters often find it helpful and reliable.")

    return contact_validate_text

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

def control_experience_detail(parsed_sections):
    experience_detail_validation_text = []
    experience_section = (
        parsed_sections.get("experience") 
        or parsed_sections.get("professional experience") 
        or "undefined"
    )
    print(experience_section)
    if experience_section:
        experience_detail_validation_text.append(find_experience_dates(experience_section))

def parse_date(date_str):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None

def find_experience_dates(experience_text):
    months = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
    date_piece = rf'(?:\d{{1,2}}[/-]\d{{4}}|{months}\s+\d{{4}}|\d{{4}})'
    date_range_re = re.compile(rf'({date_piece})\s*(?:–|-|to)\s*({date_piece})', re.I)
    date_validate_text = []
    lines = experience_text.splitlines()

    for match in date_range_re.findall(experience_text):
        start_str, end_str = match
        start_dt = parse_date(start_str)
        end_dt = parse_date(end_str)
        print(match)

        if not start_dt or not end_dt:
            date_validate_text.append(f"Date formats are incorrect.")
        if start_dt and end_dt and start_dt > end_dt:
            date_validate_text.append(f"History is logically incorrect: {start_str} > {end_str}")

    return date_validate_text