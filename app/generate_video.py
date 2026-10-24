
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT / "ignivolt_config.json"
OUTPUT_DIR = ROOT / "production" / "video_drafts"


def load_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            "ignivolt_config.json was not found."
        )

    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_video_plan(topic, duration_seconds=60):
    config = load_config()

    if not topic or not topic.strip():
        raise ValueError("Please provide a video topic.")

    engineer = config["characters"]["engineer"]
    technician = config["characters"]["technician"]

    plan = {
        "channel": config["channel"],
        "topic": topic.strip(),
        "language": config["language"],
        "aspect_ratio": config["aspect_ratio"],
        "video_style": config["video_style"],
        "status": "DRAFT_REQUIRES_HUMAN_REVIEW",
        "publishing_mode": config["publishing_mode"],
        "duration_seconds": duration_seconds,
        "characters": {
            "engineer": engineer,
            "technician": technician
        },
        "animation_rules": config["animation_rules"],
        "scene_rules": config["scene_rules"],
        "audio_rules": config["audio_rules"],
        "technical_safety": config["technical_safety"],
        "approval_checklist": config["approval_checklist"],
        "scenes": [
            {
                "scene": 1,
                "purpose": "Opening question",
                "duration_seconds": 5,
                "speaker": "technician",
                "dialogue": (
                    f"Sir, {topic.strip()} ko "
                    "sahi tarike se kaise samjhein?"
                ),
                "background_instruction": (
                    "Choose a realistic industrial background "
                    "relevant to the topic. Show no text."
                ),
                "camera": (
                    "Stable medium-wide two-character shot; "
                    "no unnecessary zoom."
                ),
                "animation": (
                    "Technician speaks with natural lip-sync "
                    "and a small hand gesture. Engineer listens, "
                    "blinks naturally and gives a slight smile."
                )
            },
            {
                "scene": 2,
                "purpose": "Technical explanation",
                "duration_seconds": max(10, duration_seconds - 15),
                "speaker": "engineer",
                "dialogue": (
                    "Chaliye, ise step by step samajhte hain. "
                    "Sabse pehle equipment aur safety conditions "
                    "ko verify karna zaroori hai."
                ),
                "background_instruction": (
                    "Use topic-specific equipment and a realistic "
                    "industrial environment. Avoid invented labels."
                ),
                "camera": (
                    "Stable medium-wide shot with restrained "
                    "movement and consistent character positions."
                ),
                "animation": (
                    "Engineer explains with measured hand gestures, "
                    "natural blinking and friendly eye contact. "
                    "Technician listens without speaking."
                )
            },
            {
                "scene": 3,
                "purpose": "Safety and conclusion",
                "duration_seconds": 10,
                "speaker": "technician",
                "dialogue": (
                    "Samajh gaya sir. Practical work mein "
                    "electrical safety follow karna zaroori hai."
                ),
                "background_instruction": (
                    "Keep the same topic-relevant environment "
                    "and realistic industrial lighting."
                ),
                "camera": (
                    "Stable two-character medium-wide shot; "
                    "no abrupt cuts or excessive zoom."
                ),
                "animation": (
                    "Technician responds with a slight smile "
                    "and a small confirming gesture. Engineer "
                    "nods naturally while listening."
                )
            }
        ]
    }

    return plan


def main():
    topic = input("Enter IGNIVOLT video topic: ").strip()
    plan = build_video_plan(topic)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / "video_plan.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(plan, file, ensure_ascii=False, indent=2)

    print(f"Draft video plan saved: {output_file}")
    print("Status: Human review required.")
    print("Note: This creates a plan, not a rendered video.")


if __name__ == "__main__":
    main()
