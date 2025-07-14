import sys
from reddit_scraper import fetch_user_data
from persona_generator import generate_persona
import os

def run(username):
    print(f" Fetching data for: {username}")
    user_data = fetch_user_data(username)

    print(" Generating Persona...")
    persona = generate_persona(user_data)

    # Clean LLM token 
    for token in ["<|start_header_id|>", "<|end_header_id|>", "assistant"]:
        persona = persona.replace(token, "")

    # Get the user's profile picture
    profile_pic_url = user_data.get("icon_img", "")

    if profile_pic_url:
        profile_pic_block = (
            "───────────────────────────────────────────────\n"
            "USER PROFILE PICTURE\n"
            f"{profile_pic_url}\n"
            "───────────────────────────────────────────────\n\n"
        )
    else:
        profile_pic_block = (
            "───────────────────────────────────────────────\n"
            " USER PROFILE PICTURE\n"
            "No profile picture available.\n"
            "───────────────────────────────────────────────\n\n"
        )

    #  Combine final output
    final_output = f"{profile_pic_block}{persona}"

    #  Save to file
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{username}_persona.txt")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(final_output)

    print(f" Persona saved to {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <reddit_username>")
    else:
        run(sys.argv[1])
