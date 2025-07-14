import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load GROQ_API_KEY from .env file

def generate_persona(data):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment.")

    # Filtering and formating comments/posts
    comment_blocks = [c for c in data["comments"] if len(c.split()) > 5][:15]
    submission_blocks = [p for p in data["submissions"] if len(p.split()) > 5][:10]

    text_blocks = comment_blocks + submission_blocks
    text_input = "\n".join(text_blocks)

    # Guardrail: to ensure model does not generate persona if data is less
    if len(text_input.strip().split()) < 20:
        return "This user has insufficient Reddit activity. Persona not generated."

    # Prompt to the model
    prompt = f"""
You are a behavioral analyst generating a Reddit-based user persona in `.txt` format.

You must:
- Dynamically infer the user's personality traits from their Reddit activity
- Adjust the personality sliders below (using 🔘) based on actual comments and posts
- DO NOT include any instructions, markdown, or explanations in the output
- Only return the formatted persona as shown

══════════════════════════════════════════════
              USER PERSONA SHEET
══════════════════════════════════════════════

Name (Handle)     : [Assumed name or Reddit handle]  
Age Range         : [e.g. 25–34]  
Archetype         : [e.g. Curious Commentator | Tech Explorer]  
Reddit Activity   : [e.g. 42 comments, 6 posts]  
Tone              : [e.g. Logical, Witty, Analytical]

──────────────────────────────────────────────
QUOTE
──────────────────────────────────────────────
"[A short, representative quote from their post or comment]"

──────────────────────────────────────────────
GOALS & NEEDS
──────────────────────────────────────────────
• [User's goal 1]  
• [User's goal 2]  
• [User's goal 3]

──────────────────────────────────────────────
FRUSTRATIONS
──────────────────────────────────────────────
• [Common complaint or annoyance]  
• [Behavior they criticize or avoid]  
• [Reddit patterns they push against]

──────────────────────────────────────────────
MOTIVATIONS
──────────────────────────────────────────────
• [What drives this user's Reddit engagement]  
• [What they value or seek in communities]  
• [Internal or external motivators]

──────────────────────────────────────────────
PERSONALITY SLIDERS
──────────────────────────────────────────────
INTROVERT     🔘──────────── EXTROVERT  
INTUITION     ──────🔘────── SENSING  
FEELING       ─────🔘─────── THINKING  
PERCEIVING    ─────────🔘─── JUDGING

(The 🔘 markers must reflect actual analysis of the user’s tone, language, and Reddit behavior.)

──────────────────────────────────────────────
MEDIA BEHAVIOR
──────────────────────────────────────────────
• [Do they post media? What kind?]  
• [How frequently or in what context?]

──────────────────────────────────────────────
PERSONALITY TRAITS (with evidence)
──────────────────────────────────────────────
• [Trait 1] — based on: “[Reddit comment]”  
• [Trait 2] — based on: “[Reddit post]”  
• [Trait 3] — based on: “[Reddit comment]”

──────────────────────────────────────────────
INSIGHTS
──────────────────────────────────────────────
• Top subreddits     : [r/example1, r/example2]  
• Avg. comment length: [Short / Medium / Long]  
• Writing style      : [Casual / Formal / Analytical / Sarcastic]  
• Community role     : [Initiator / Supporter / Responder / Passive]

══════════════════════════════════════════════

If the user's Reddit data is under 20 words, return only:
"Not enough Reddit activity to generate a meaningful persona."

Reddit Activity:
{text_input}
""".strip()



    
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a behavioral analyst."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
