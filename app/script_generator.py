
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "production" / "video_drafts"


TOPIC_LIBRARY = {
    "vfd": {
        "title": "VFD Motor Not Starting Troubleshooting",
        "steps": [
            (
                "Fault code check",
                "Sabse pehle VFD display par fault ya alarm code check karein. "
                "Code ko note karein aur us model ke manual se uska meaning verify karein."
            ),
            (
                "Run command",
                "Ab verify karein ki drive ko run command mil rahi hai ya nahi. "
                "Local ya remote mode aur control source settings bhi check karein."
            ),
            (
                "Safety interlocks",
                "Emergency stop, permissive aur safety interlocks ka status "
                "approved control diagram ke according verify karein."
            ),
            (
                "Reference signal",
                "Frequency reference check karein. Analog signal, communication "
                "ya keypad reference mein se jo control method use ho raha hai, "
                "usi ke according verify karein."
            ),
            (
                "Output and motor",
                "Drive status aur output frequency dekhein. Motor aur power "
                "circuit ki checking sirf proper isolation aur qualified "
                "procedure ke according karein."
            )
        ]
    },
    "plc": {
        "title": "PLC Troubleshooting",
        "steps": [
            ("Power supply", "PLC ki supply indication aur specified voltage verify karein."),
            ("CPU status", "CPU ke RUN, STOP ya ERROR indicators observe karein."),
            ("Input signals", "Input status ko actual sensor condition aur electrical drawing se compare karein."),
            ("Program and output", "Logic conditions aur output status approved program ke according check karein."),
            ("Field device", "Field wiring aur actuator ko approved isolation procedure follow karke inspect karein.")
        ]
    },
    "motor": {
        "title": "Motor Troubleshooting",
        "steps": [
            ("Complaint", "Motor ka exact symptom note karein: no start, overheating, noise ya vibration."),
            ("Protection", "Protection relay aur starter ke trip indications record karein."),
            ("Supply", "Qualified person approved procedure ke according supply condition verify kare."),
            ("Mechanical condition", "Isolation ke baad shaft, coupling aur load ki mechanical condition check karein."),
            ("Test results", "Insulation aur winding tests sirf suitable instruments aur approved procedure se karein.")
        ]
    },
    "transformer": {
        "title": "Transformer Troubleshooting",
        "steps": [
            ("Initial indications", "Alarm, trip indication, temperature aur unusual noise observe karein."),
            ("Protection", "Relay indications aur recorded fault information review karein."),
            ("Load", "Load current aur phase balance ko equipment ratings ke saath compare karein."),
            ("Cooling", "Cooling fans, pumps aur ventilation status check karein, where applicable."),
            ("Inspection", "Internal inspection ya electrical testing sirf isolation aur approved safety procedure ke baad karein.")
        ]
    }
}


def select_topic(topic):
    text = topic.lower()

    if "vfd" in text or "drive" in text:
        return TOPIC_LIBRARY["vfd"]
    if "plc" in text:
        return TOPIC_LIBRARY["plc"]
    if "motor" in text:
        return TOPIC_LIBRARY["motor"]
    if "transformer" in text:
        return TOPIC_LIBRARY["transformer"]

    return {
        "title": topic,
        "steps": [
            ("Basic concept", f"Sabse pehle {topic} ka basic function aur operating principle samjhein."),
            ("Main components", "Important components aur unke functions ko identify karein."),
            ("Normal operation", "Normal operating indications ko manufacturer documentation se verify karein."),
            ("Troubleshooting", "Symptoms aur observations record karke approved troubleshooting procedure follow karein."),
            ("Safety", "Electrical safety, required isolation aur relevant approved procedures follow karein.")
        ]
    }


def estimate_words(text):
    return len(re.findall(r"\b[\w'-]+\b", text))


def build_script(topic, duration_seconds):
    topic = topic.strip()

    if not topic:
        raise ValueError("Please enter a topic.")

    if duration_seconds not in (40, 60, 600):
        raise ValueError("Duration must be 40, 60 or 600 seconds.")

    library = select_topic(topic)

    if duration_seconds == 600:
        video_type = "Long YouTube Video"
        aspect_ratio = "16:9"
        hook_duration = 20
        conclusion_duration = 20
        explanation_target = 40
    else:
        video_type = "YouTube Short"
        aspect_ratio = "9:16"
        hook_duration = 5
        conclusion_duration = 5
        explanation_target = 10

    explanation_duration = (
        duration_seconds - hook_duration - conclusion_duration
    )

    # Create scene durations that add up exactly to the requested duration.
    durations = []
    remaining = explanation_duration

    while remaining:
        part = min(explanation_target, remaining)
        durations.append(part)
        remaining -= part

    common_visual = (
        "Realistic cinematic 3D industrial electrical training. "
        "Use the approved IGNIVOLT reference image. WHITE HELMET and "
        "NAVY-BLUE UNIFORM is the Lead Engineer. YELLOW HELMET and "
        "ORANGE UNIFORM is the Technician. Preserve faces, helmet colors, "
        "uniforms and IGNIVOLT branding. Engineer asks questions first; "
        "Technician listens and answers when instructed. Natural gestures, "
        "stable camera, relevant equipment, no subtitles, no random text. "
        "Show safe and technically plausible work only."
    )

    scenes = [
        {
            "scene": 1,
            "purpose": "Hook",
            "duration_seconds": hook_duration,
            "speaker": "engineer",
            "dialogue": (
                f"VFD ON hai, lekin motor start nahi ho rahi! "
                f"Topic hai {topic}. Batao, technician, sabse pehle "
                "kya check karoge?"
            ),
            "visual_prompt": (
                common_visual + " The white-helmet Lead Engineer asks "
                "the question. The yellow-helmet Technician listens silently."
            )
        }
    ]

    for index, duration in enumerate(durations):
        title, explanation = library["steps"][index % len(library["steps"])]

        scenes.append({
            "scene": len(scenes) + 1,
            "purpose": f"Technical Step {index + 1}: {title}",
            "duration_seconds": duration,
            "speaker_sequence": ["engineer", "technician"],
            "dialogue": (
                f"Engineer: {title}. {explanation}\n"
                "Technician: Samajh gaya sir. Is point ko practical "
                "troubleshooting mein verify karna zaroori hai."
            ),
            "visual_prompt": (
                common_visual + f" Demonstrate the topic-specific step: "
                f"{title}. The engineer explains; the technician listens "
                "and then responds. Only the active speaker moves their lips."
            ),
            "review_required": True
        })

    scenes.append({
        "scene": len(scenes) + 1,
        "purpose": "Conclusion",
        "duration_seconds": conclusion_duration,
        "speaker_sequence": ["technician", "engineer"],
        "dialogue": (
            "Technician: Samajh gaya sir! Main fault indications aur "
            "approved procedure ke according checks karunga.\n"
            "Engineer: Bilkul. Safety ko priority dein aur manufacturer "
            "manual follow karein. Aise hi electrical knowledge ke liye "
            "IGNIVOLT ko follow karein."
        ),
        "visual_prompt": (
            common_visual + " The technician summarizes first. "
            "The engineer delivers the final safety reminder. "
            "Both characters end facing the camera."
        )
    })

    total = sum(scene["duration_seconds"] for scene in scenes)

    if total != duration_seconds:
        raise RuntimeError("Scene duration calculation failed.")

    script_text = "\n\n".join(
        f"SCENE {scene['scene']} ({scene['duration_seconds']} seconds)\n"
        f"{scene['dialogue']}"
        for scene in scenes
    )

    return {
        "channel": "IGNIVOLT",
        "topic": topic,
        "matched_topic_template": library["title"],
        "video_type": video_type,
        "language": "Hindi + Hinglish",
        "aspect_ratio": aspect_ratio,
        "duration_seconds": duration_seconds,
        "planned_duration_seconds": total,
        "planned_scene_count": len(scenes),
        "status": "DRAFT_REQUIRES_HUMAN_REVIEW",
        "publishing_mode": "human_approval_required",
        "voiceover_language": "Hindi + Hinglish",
        "voiceover_note": (
            "This file contains dialogue text only. It does not create "
            "audible voice-over, animation, lip-sync or a rendered video."
        ),
        "estimated_dialogue_words": estimate_words(script_text),
        "scenes": scenes,
        "script_text": script_text,
        "important_note": (
            "Offline template-based draft. Verify technical instructions "
            "against the exact equipment manual before training or use. "
            "Topics without a dedicated template receive a generic draft."
        )
    }


def main():
    topic = input("Enter IGNIVOLT video topic: ").strip()

    print("\nChoose duration:")
    print("1. 40 seconds")
    print("2. 60 seconds")
    print("3. 10 minutes")

    choice = input("Enter 1, 2 or 3: ").strip()
    options = {"1": 40, "2": 60, "3": 600}

    if choice not in options:
        raise ValueError("Choose 1, 2 or 3.")

    plan = build_script(topic, options[choice])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / "script_draft.json"

    output_file.write_text(
        json.dumps(plan, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"\nScript draft saved: {output_file}")
    print(f"Duration: {plan['planned_duration_seconds']} seconds")
    print(f"Scenes: {plan['planned_scene_count']}")
    print("Human review required.")
    print("No video or audio has been generated.")


if __name__ == "__main__":
    main()
      
