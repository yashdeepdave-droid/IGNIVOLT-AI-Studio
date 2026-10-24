
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

    if not isinstance(duration_seconds, int):
        raise ValueError("Duration must be an integer.")

    if duration_seconds not in (40, 60, 600):
        raise ValueError(
            "Choose 40 seconds, 60 seconds, or 600 seconds."
        )

    config = load_config()

    if duration_seconds == 600:
        video_type = "Long YouTube Video"
        aspect_ratio = "16:9"
        hook_duration = 20
        conclusion_duration = 20
        target_scene_duration = 20
    else:
        video_type = "YouTube Short"
        aspect_ratio = "9:16"
        hook_duration = 5
        conclusion_duration = 5
        target_scene_duration = 10

    explanation_duration = (
        duration_seconds - hook_duration - conclusion_duration
    )

    # Divide the explanation time across scenes.
    scene_durations = []
    remaining = explanation_duration

    while remaining > 0:
        scene_length = min(target_scene_duration, remaining)
        scene_durations.append(scene_length)
        remaining -= scene_length

    # These are structured script templates, not AI-generated research.
    # Replace the topic-specific dialogue with verified details
    # before using the plan for technical training.

    scenes = []

    common_visual = (
        "Realistic cinematic 3D electrical training in an industrial "
        "workshop. Preserve the approved IGNIVOLT character reference "
        "image. WHITE HELMET and NAVY-BLUE UNIFORM: Lead Electrical "
        "Engineer. YELLOW HELMET and ORANGE UNIFORM: Technician. "
        "Keep faces, body proportions, uniform colors and IGNIVOLT "
        "helmet branding consistent. Natural blinking, subtle gestures, "
        "stable camera, relevant industrial equipment. No subtitles "
        "or random text. Show safe electrical practices."
    )

    # Scene 1: Hook — engineer asks, technician listens.
    scenes.append({
        "scene": 1,
        "purpose": "Hook",
        "duration_seconds": hook_duration,
        "speaker": "engineer",
        "dialogue": (
            f"Aaj ka topic hai {topic}. "
            "Agar aapse interview mein iske baare mein poochha jaaye, "
            "to kya aap iska practical answer de paayenge? "
            "Chaliye, step by step samajhte hain."
        ),
        "visual_prompt": (
            f"{common_visual} Topic: {topic}. The white-helmet Lead "
            "Engineer asks the opening question. The yellow-helmet "
            "Technician listens silently. Engineer speaks first."
        ),
        "voice_language": "Hindi + Hinglish",
        "lip_sync_required": True
    })

    # Explanation scenes with concrete starter dialogue.
    for index, scene_duration in enumerate(scene_durations, start=1):
        scene_number = index + 1

        if index == 1:
            dialogue = (
                f"Sabse pehle, {topic} ka basic concept samajhte hain. "
                "Is topic mein equipment ka function, operating "
                "principle aur safety requirements samajhna zaroori hai."
            )
        elif index == 2:
            dialogue = (
                "Ab important components ko identify karein. Har "
                "component ka function samjhein aur manufacturer ki "
                "approved documentation se details verify karein."
            )
        elif index == 3:
            dialogue = (
                "Practical troubleshooting mein symptoms ko observe "
                "karein, relevant indications record karein aur "
                "approved procedure ke according checks karein."
            )
        elif index == 4:
            dialogue = (
                "Ek important baat: electrical equipment par kaam "
                "karne se pehle required isolation, lockout-tagout "
                "aur absence-of-voltage verification follow karein."
            )
        else:
            dialogue = (
                f"Ab {topic} ke agle important point ko samajhte hain. "
                "Correct procedure follow karein, observations note "
                "karein aur technical details ko reliable documentation "
                "se verify karein."
            )

        scenes.append({
            "scene": scene_number,
            "purpose": f"Explanation Part {index}",
            "duration_seconds": scene_duration,
            "speaker": "engineer",
            "dialogue": dialogue,
            "visual_prompt": (
                f"{common_visual} Demonstrate explanation part {index} "
                f"of {topic}. The white-helmet Lead Engineer explains "
                "the equipment to the yellow-helmet Technician. The "
                "Technician listens with his mouth closed. Show only "
                "relevant, technically plausible equipment."
            ),
            "voice_language": "Hindi + Hinglish",
            "lip_sync_required": True,
            "review_required": True
        })

    # Final scene: technician summarizes, engineer concludes.
    scenes.append({
        "scene": len(scenes) + 1,
        "purpose": "Conclusion",
        "duration_seconds": conclusion_duration,
        "speaker_sequence": ["technician", "engineer"],
        "dialogue": (
            "Technician: Samajh gaya sir! Correct procedure aur safety "
            "follow karna zaroori hai.\n"
            "Engineer: Bilkul. Practical work hamesha approved "
            "procedure ke according karein. Aise hi electrical "
            "knowledge ke liye IGNIVOLT ko follow karein."
        ),
        "visual_prompt": (
            f"{common_visual} Topic: {topic}. The yellow-helmet "
            "Technician speaks first and summarizes the lesson. Then "
            "the white-helmet Lead Engineer gives the final tip. "
            "Only the active speaker moves his lips. End with both "
            "characters facing the camera."
        ),
        "voice_language": "Hindi + Hinglish",
        "lip_sync_required": True
    })

    planned_duration = sum(
        scene["duration_seconds"] for scene in scenes
    )

    if planned_duration != duration_seconds:
        raise RuntimeError("Scene duration total is incorrect.")

    plan = {
        "channel": config["channel"],
        "topic": topic,
        "video_type": video_type,
        "language": "Hindi + Hinglish",
        "aspect_ratio": aspect_ratio,
        "video_style": config["video_style"],
        "duration_seconds": duration_seconds,
        "duration_minutes": duration_seconds / 60,
        "status": "DRAFT_REQUIRES_HUMAN_REVIEW",
        "publishing_mode": "human_approval_required",
        "characters": config["characters"],
        "character_consistency": config.get(
            "character_consistency", []
        ),
        "animation_rules": config["animation_rules"],
        "scene_rules": config.get("scene_rules", []),
        "audio_rules": config["audio_rules"],
        "technical_safety": config["technical_safety"],
        "approval_checklist": config["approval_checklist"],
        "planned_scene_count": len(scenes),
        "planned_duration_seconds": planned_duration,
        "scenes": scenes,
        "important_note": (
            "This creates a structured draft plan with starter dialogue "
            "and visual prompts. The dialogue is not a complete, "
            "topic-verified technical script. Human review and topic "
            "specific research are required. This code does not "
            "generate actual video, audio, images or lip-sync."
        )
    }

    return plan


def main():
    topic = input("Enter IGNIVOLT video topic: ").strip()

    print("\nChoose video duration:")
    print("1. 40 seconds")
    print("2. 60 seconds")
    print("3. 10 minutes")

    choice = input("Enter 1, 2 or 3: ").strip()

    duration_options = {
        "1": 40,
        "2": 60,
        "3": 600
    }

    if choice not in duration_options:
        raise ValueError("Please choose 1, 2 or 3.")

    duration = duration_options[choice]
    plan = build_video_plan(topic, duration)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / "video_plan.json"

    output_file.write_text(
        json.dumps(plan, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"\nVideo plan saved: {output_file}")
    print(f"Video type: {plan['video_type']}")
    print(f"Duration: {duration} seconds")
    print(f"Scenes: {plan['planned_scene_count']}")
    print("Status: Human review required.")
    print("No video has been generated or published.")


if __name__ == "__main__":
    main()
    
