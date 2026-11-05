import os, json
def create_edit_notes(script):
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return "Claude API key not configured. Basic edit completed with voice-synced captions."
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        msg = client.messages.create(
            model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5"),
            max_tokens=900,
            system=("You are a professional short-form video editor. Return concise JSON with "
                    "hook, scene_breakdown, visual_suggestions, sound_design, caption_style. "
                    "Do not claim to have rendered anything. Keep suggestions practical."),
            messages=[{"role":"user","content":"Create an edit plan for this script:\n"+script}]
        )
        return msg.content[0].text
    except Exception as e:
        return "Claude planning unavailable: " + str(e)[:250]
