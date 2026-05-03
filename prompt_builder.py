"""
prompt_builder.py
-----------------
Responsible for assembling the prompts sent to the OpenAI API.
All prompt logic lives HERE — never in app.py.
"""


def build_company_lookup_prompt(company_name):
    """
    Returns a prompt used with gpt-4o-search-preview to fetch real company info from the web.

    Parameter:
        company_name - e.g. "Perennial Systems"

    Returns:
        str — a single user prompt (no system prompt needed for web search model)
    """
    return (
        f"Search the web for '{company_name}' and write a concise 3-4 sentence professional "
        f"company description suitable for a job posting. "
        f"Include what the company does, its mission, and the clients or markets it serves. "
        f"Return only the description text — no headings, no bullet points, no extra commentary."
    )


def build_jd_prompt(role_title, seniority, industry, skills, responsibilities, nice_to_have, company_description=""):
    """
    Builds and returns the system + user prompts for JD generation.

    Parameters (all strings, coming from the Gradio form):
        role_title          - e.g. "Backend Engineer"
        seniority           - e.g. "Senior"
        industry            - e.g. "Fintech"
        skills              - e.g. "Java, Spring Boot, Kafka, PostgreSQL"
        responsibilities    - e.g. "Build APIs, mentor juniors, own deployments"
        nice_to_have        - e.g. "AWS experience, open source contributions"
        company_description - e.g. "Perennial Systems is a..." (optional, from web lookup)

    Returns:
        tuple (system_prompt, user_prompt)
    """

    # Build the section list dynamically — only include "About the Company"
    # if we actually have a company description to put in it
    if company_description:
        sections = """## Job Title
## About the Company
## About the Role
## Key Responsibilities
## Required Skills & Experience
## Nice to Have
## What We Offer"""
    else:
        sections = """## Job Title
## About the Role
## Key Responsibilities
## Required Skills & Experience
## Nice to Have
## What We Offer"""

    # --- SYSTEM PROMPT ---
    system_prompt = f"""You are an expert HR professional and technical recruiter with 15 years of experience writing job descriptions for top tech companies.

When given role details, you produce clear, professional, and structured job descriptions that:
- Are inclusive and free of biased language
- Are specific enough to attract qualified candidates
- Follow this EXACT output structure (use these markdown headings):

{sections}

Keep the tone professional but human. Each section should be concise — bullet points where appropriate.
Do not add any commentary before or after the JD. Output the JD only."""

    # --- COMPANY SECTION ---
    # Only added to the user prompt if a company description was fetched
    company_section = ""
    if company_description:
        company_section = f"\nCompany Description (use this for the 'About the Company' section):\n{company_description}\n"

    # --- USER PROMPT ---
    user_prompt = f"""Please generate a professional job description using the following details:

Role Title: {role_title}
Seniority Level: {seniority}
Industry: {industry}
{company_section}
Key Skills Required:
{skills}

Core Responsibilities:
{responsibilities}

Nice to Have:
{nice_to_have}

Generate the full job description now."""

    return system_prompt, user_prompt
