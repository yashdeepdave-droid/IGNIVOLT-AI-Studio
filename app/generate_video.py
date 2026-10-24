
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT / "ignivolt_config.json"
OUTPUT_DIR = ROOT / "production" / "video_drafts"


def load_config():
    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_video_plan(topic, duration_seconds=60):
    topic = topic.strip()

    if not topic:
        raise ValueError("Please enter a video topic.")

    if duration_seconds < 15:
        raise ValueError("Video duration must be at least 15 seconds.")

    config = load_config()

    scenes = [
        {
            "scene": 1,
            "purpose": "Hook",
            "duration_seconds": 5,
            "speaker": "technician",
            "dialogue": (
                f"Sir, {topic} ko lekar ek important sawal hai. "
                "Ise practically kaise samjhein?"
            ),
            "visual_prompt": (
                f"Vertical 9:16 cinematic realistic 3D industrial scene "
                f"about {topic}. Show the approved IGNIVOLT engineer "
                "and technician characters together. Technician asks "
                "a question; engineer listens. Preserve both characters' "
                "faces, uniforms and helmet colors. Natural expressions, "
                "stable medium-wide camera. No text or subtitles."
            )
        },
        {
            "scene": 2,
            "purpose": "Explanation",
            "duration_seconds": duration_seconds - 15,
            "speaker": "engineer",
            "dialogue": (
                f"Chaliye, {topic} ko step by step samajhte hain. "
                "Sabse pehle equipment ki condition aur safety "
                "requirements verify karein. Uske baad relevant "
                "components ko identify karke unka function samjhein. "
                "Practical work hamesha approved procedure ke according karein."
            ),
            "visual_prompt": (
                f"Vertical 9:16 realistic 3D industrial training scene "
                f"demonstrating {topic}. Engineer explains relevant "
                "equipment to the technician using natural hand gestures. "
                "Technician listens without speaking. Preserve approved "
                "character designs and use a topic-relevant background. "
                "Show only technically plausible equipment. No text."
            )
        },
        {
            "scene": 3,
            "purpose": "Conclusion",
            "duration_seconds": 10,
            "speaker": "technician",
            "dialogue": (
                "Samajh gaya sir! Practical work mein correct procedure "
                "aur electrical safety dono zaroori hain. Aise hi "
                "electrical knowledge ke liye IGNIVOLT ko follow karein."
            ),
            "visual_prompt": (
                f"Vertical 9:16 realistic 3D industrial scene about {topic}. "
                "Both approved IGNIVOLT characters stand together. "
                "Technician responds with a natural confirming gesture; "
                "engineer nods. Consistent faces, uniforms and helmets, "
                "stable medium-wide camera, natural expressions. No text."
            )
        }
    ]

    plan = {
        "channel": config["channel"],
        "topic": topic,
        "language": config["language"],
        "aspect_ratio": "9:16",
        "video_style": config["video_style"],
        "duration_seconds": duration_seconds,
        "status": "DRAFT_REQUIRES_HUMAN_REVIEW",
        "publishing_mode": "human_approval_required",
        "characters": config["characters"],
        "animation_rules": config["animation_rules"],
        "audio_rules": config["audio_rules"],
        "technical_safety": config["technical_safety"],
        "approval_checklist": config["approval_checklist"],
        "scenes": scenes,
        "important_note": (
            "This file creates a video plan only. It does not generate "
            "images, audio, animation or a rendered video."
        )
    }

    return plan


def main():
    topic = input("Enter IGNIVOLT video topic: ").strip()

    plan = build_video_plan(topic)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / "video_plan.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(plan, file, ensure_ascii=False, indent=2)

    print(f"Draft plan saved: {output_file}")
    print("Status: Human review required.")
    print("No video has been generated or published.")


if __name__ == "__main__":
    main()
