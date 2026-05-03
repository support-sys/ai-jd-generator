"""
app.py
------
Main entry point. Builds the Gradio web UI and calls the OpenAI API.
Prompt logic lives in prompt_builder.py — not here.
"""

import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
from prompt_builder import build_company_lookup_prompt, build_jd_prompt

# load_dotenv() reads your .env file and puts the key into os.environ
# Think of it like loading a .properties file in Spring Boot
load_dotenv()


def lookup_company(client, company_name):
    """
    Step 1 (optional): Uses gpt-4o-search-preview to fetch real company info from the web.
    Returns a company description string, or empty string if company_name is blank.

    Java analogy: like calling an external REST service before your main business logic.
    """
    if not company_name.strip():
        return ""  # company field was left empty — skip the lookup

    prompt = build_company_lookup_prompt(company_name)

    # gpt-4o-search-preview is a special model with built-in web search
    # It doesn't support 'temperature' — just pass the messages
    response = client.chat.completions.create(
        model="gpt-4o-search-preview",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content


def generate_jd(company_name, role_title, seniority, industry, skills, responsibilities, nice_to_have):
    """
    Called every time the user clicks Generate.
    Step 1: look up company on the web (if provided).
    Step 2: build prompts and call gpt-4o to generate the JD.
    """

    # Basic validation — required fields must not be empty
    if not role_title.strip() or not skills.strip() or not responsibilities.strip():
        return "Please fill in at least: Role Title, Key Skills, and Responsibilities."

    # One shared client for both API calls
    client = OpenAI()

    # Step 1 — optional company web lookup
    company_description = lookup_company(client, company_name)

    # Step 2 — build prompts (company_description passed in if available)
    system_prompt, user_prompt = build_jd_prompt(
        role_title, seniority, industry, skills, responsibilities, nice_to_have, company_description
    )

    # Step 3 — call gpt-4o to generate the full JD
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content


# --- GRADIO UI ---
with gr.Blocks(title="AI Job Description Generator") as app:

    gr.Markdown("# 💼 AI Job Description Generator")
    gr.Markdown("Fill in the role details below and click **Generate** to create a professional JD.")

    # Company name — optional, triggers a live web lookup
    company_name = gr.Textbox(
        label="Hiring For",
        placeholder="Name of the Company"
    )

    # Row 1: Role title + seniority
    with gr.Row():
        role_title = gr.Textbox(label="Role Title *", placeholder="e.g. Backend Engineer")
        seniority  = gr.Dropdown(
            label="Seniority Level",
            choices=["Junior", "Mid-level", "Senior", "Lead", "Principal", "Head of"],
            value="Senior"
        )

    # Row 2: Industry + nice to have
    with gr.Row():
        industry     = gr.Textbox(label="Industry", placeholder="e.g. Fintech, HealthTech, SaaS")
        nice_to_have = gr.Textbox(label="Nice to Have", placeholder="e.g. AWS experience, open source contributions")

    skills = gr.Textbox(
        label="Key Skills Required *",
        placeholder="e.g. Java, Spring Boot, Kafka, PostgreSQL, REST APIs",
        lines=2
    )

    responsibilities = gr.Textbox(
        label="Core Responsibilities *",
        placeholder="e.g. Design and build scalable APIs, mentor junior developers, own CI/CD pipelines",
        lines=3
    )

    generate_btn = gr.Button("Generate Job Description", variant="primary")

    gr.Markdown("---")
    gr.Markdown("### Generated Job Description")

    output = gr.Textbox(
        label="Output (copy from here)",
        lines=30,
    )

    # Wire the button — inputs must match the parameter order of generate_jd()
    generate_btn.click(
        fn=generate_jd,
        inputs=[company_name, role_title, seniority, industry, skills, responsibilities, nice_to_have],
        outputs=output
    )

# Launch the app
if __name__ == "__main__":
    app.launch()
