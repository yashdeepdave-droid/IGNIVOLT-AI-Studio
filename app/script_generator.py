
import re


CHANNEL = "IGNIVOLT"
SUPPORTED_DURATIONS = (40, 60, 600)

CHARACTER_STYLE = (
    "Realistic cinematic 3D industrial electrical training. Use the approved "
    "IGNIVOLT character reference image. Lead Engineer: same youthful male "
    "face, white hard hat with IGNIVOLT lightning logo, navy-blue industrial "
    "uniform with reflective strips and black gloves. Technician: same "
    "youthful male face, yellow hard hat and orange coverall with reflective "
    "strips. Preserve faces, proportions, uniforms and branding. Natural "
    "blinking, subtle expressions and hand gestures. Only the active speaker "
    "moves their lips; the listener keeps lips still. Stable medium shot, "
    "no abrupt cuts, no subtitles, no captions and no random text. Show "
    "electrically safe, technically plausible actions."
)


VFD_SCENES = [
    {
        "purpose": "Hook",
        "speaker": "engineer",
        "dialogue": (
            "VFD ON hai, lekin motor start nahi ho rahi! "
            "Ye electrical interviews mein bhi important question hai. "
            "Chaliye, step-by-step troubleshooting karte hain."
        ),
        "visual": (
            "Show the VFD powered with a stationary motor. "
            "The engineer asks the question while the technician listens."
        ),
    },
    {
        "purpose": "Step 1: Check fault history",
        "speaker": "engineer",
        "dialogue": (
            "Sabse pehle drive display par fault ya alarm check karein. "
            "Code note karein aur exact VFD manual se uska meaning verify karein."
        ),
        "visual": (
            "Show the engineer indicating the VFD display. Do not invent "
            "a fault code or display unreadable technical text."
        ),
    },
    {
        "purpose": "Step 2: Verify run command",
        "speaker": "technician",
        "dialogue": (
            "Sir, ab run command verify karunga. Drive local mode mein hai "
            "ya remote, aur command keypad, PLC ya terminal se aa rahi hai?"
        ),
        "visual": (
            "The technician asks while pointing toward the drive controls. "
            "The engineer listens silently."
        ),
    },
    {
        "purpose": "Step 3: Check interlocks",
        "speaker": "engineer",
        "dialogue": (
            "Bilkul. Emergency stop, permissive aur safety interlocks ka "
            "status approved control diagram ke according verify karein."
        ),
        "visual": (
            "Show the engineer reviewing the control panel and approved "
            "control diagram. Do not bypass any safety interlock."
        ),
    },
    {
        "purpose": "Step 4: Check frequency reference",
        "speaker": "technician",
        "dialogue": (
            "Agar command mil rahi hai, toh frequency reference check karunga. "
            "Keypad, analog input ya communication source ko configured settings "
            "ke according verify karna hoga."
        ),
        "visual": (
            "The technician indicates the configured frequency reference "
            "controls while the engineer listens."
        ),
    },
    {
        "purpose": "Step 5: Output and safety",
        "speaker": "engineer",
        "dialogue": (
            "Last mein drive status aur output frequency check karein. "
            "Power circuit ki inspection se pehle isolation, lockout-tagout "
            "aur qualified-person procedure follow karein. Follow IGNIVOLT!"
        ),
        "visual": (
            "Show the engineer giving a final safety reminder beside the "
            "VFD and motor. Both characters face the camera at the end."
        ),
    },
]


PLC_SCENES = [
    {
        "purpose": "Hook",
        "speaker": "engineer",
        "dialogue": (
            "PLC power ON hai, lekin machine ka output nahi chal raha! "
            "Aaiye, basic troubleshooting ke important steps samajhte hain."
        ),
        "visual": "Show a PLC panel with an inactive output and both characters.",
    },
    {
        "purpose": "Step 1: CPU status",
        "speaker": "technician",
        "dialogue": (
            "Sir, sabse pehle CPU status LEDs check karunga aur "
            "fault indication ko PLC manual se verify karunga."
        ),
        "visual": "Show the technician inspecting CPU status indicators.",
    },
    {
        "purpose": "Step 2: Program status",
        "speaker": "engineer",
        "dialogue": (
            "Sahi. CPU RUN ya STOP status, program diagnostics aur "
            "available fault messages check karein."
        ),
        "visual": "Show the engineer reviewing PLC diagnostics on a programming device.",
    },
    {
        "purpose": "Step 3: Input signals",
        "speaker": "technician",
        "dialogue": (
            "Ab input status ko actual sensor condition aur electrical "
            "drawing ke saath compare karunga."
        ),
        "visual": "Show input indicators and a sensor on a training setup.",
    },
    {
        "purpose": "Step 4: Output logic",
        "speaker": "engineer",
        "dialogue": (
            "Phir program logic, permissives aur output status verify karein. "
            "Interlocks ko kabhi bypass na karein."
        ),
        "visual": "Show the engineer explaining PLC logic and interlocks.",
    },
    {
        "purpose": "Conclusion",
        "speaker": "technician",
        "dialogue": (
            "Samajh gaya sir. Status, diagnostics, inputs aur outputs "
            "systematically check karunga. Electrical knowledge ke liye IGNIVOLT follow karein!"
        ),
        "visual": "Both characters face the camera beside the PLC training panel.",
    },
]


MOTOR_SCENES = [
    {
        "purpose": "Hook",
        "speaker": "engineer",
        "dialogue": (
            "Three-phase motor start nahi ho rahi? Guess karne ke bajay "
            "systematic troubleshooting karte hain."
        ),
        "visual": "Show a stationary industrial three-phase motor.",
    },
    {
        "purpose": "Step 1: Protection status",
        "speaker": "technician",
        "dialogue": (
            "Sir, overload relay, breaker aur protection trip indication "
            "ko panel status aur manual se verify karunga."
        ),
        "visual": "Show protective devices in a closed electrical panel.",
    },
    {
        "purpose": "Step 2: Control circuit",
        "speaker": "engineer",
        "dialogue": (
            "Control supply, start command aur stop circuit ko approved "
            "wiring diagram ke according check karein."
        ),
        "visual": "Show a control schematic beside a training panel.",
    },
    {
        "purpose": "Step 3: Contactor",
        "speaker": "technician",
        "dialogue": (
            "Agar contactor operate nahi karta, toh coil control aur "
            "interlocks ko safe test procedure se verify karunga."
        ),
        "visual": "Show a contactor trainer; do not show exposed live conductors.",
    },
    {
        "purpose": "Step 4: Motor condition",
        "speaker": "engineer",
        "dialogue": (
            "Motor aur power circuit ki inspection sirf isolation, "
            "lockout-tagout aur qualified procedure ke baad karein."
        ),
        "visual": "Show an isolated motor being inspected by a qualified technician.",
    },
    {
        "purpose": "Conclusion",
        "speaker": "technician",
        "dialogue": (
            "Samajh gaya sir. Protection, control command aur motor condition "
            "ko sequence mein check karunga. Follow IGNIVOLT!"
        ),
        "visual": "Both characters stand beside the motor and face the camera.",
    },
]


TRANSFORMER_SCENES = [
    {
        "purpose": "Hook",
        "speaker": "engineer",
        "dialogue": (
            "Transformer alarm ya abnormal heating dikha raha hai? "
            "Pehle indication ko samjhein, phir approved procedure follow karein."
        ),
        "visual": "Show an industrial transformer and its monitoring instruments.",
    },
    {
        "purpose": "Step 1: Alarm indication",
        "speaker": "technician",
        "dialogue": (
            "Sir, temperature, oil level aur available protection alarms "
            "ko equipment manual ke according verify karunga."
        ),
        "visual": "Show transformer gauges and alarm indicators without invented readings.",
    },
    {
        "purpose": "Step 2: Load condition",
        "speaker": "engineer",
        "dialogue": (
            "Load current aur phase-wise loading ko rated limits aur "
            "site operating procedure ke saath compare karein."
        ),
        "visual": "Show an engineer reviewing transformer load readings.",
    },
    {
        "purpose": "Step 3: Cooling system",
        "speaker": "technician",
        "dialogue": (
            "Cooling fans, pumps aur ventilation ka status check karunga, "
            "agar ye equipment mein fitted hain."
        ),
        "visual": "Show the fitted transformer cooling equipment operating normally.",
    },
    {
        "purpose": "Step 4: Protection response",
        "speaker": "engineer",
        "dialogue": (
            "Protection trip ko bina cause samjhe reset na karein. "
            "Event records aur approved troubleshooting procedure follow karein."
        ),
        "visual": "Show the engineer reviewing protection records at a safe distance.",
    },
    {
        "purpose": "Conclusion",
        "speaker": "technician",
        "dialogue": (
            "Samajh gaya sir. Alarm, load aur cooling condition verify karunga. "
            "Safety aur manufacturer instructions ko priority dunga. Follow IGNIVOLT!"
        ),
        "visual": "Both characters face the camera beside the transformer.",
    },
]


GENERIC_SCENES = [
    {
        "purpose": "Hook",
        "speaker": "engineer",
        "dialogue": (
            "Electrical equipment mein fault aaye, toh guesswork nahi "
            "systematic troubleshooting zaroori hai. Aaiye, basic steps samjhein."
        ),
        "visual": "Show the topic's relevant industrial electrical equipment.",
    },
    {
        "purpose": "Step 1: Observe the symptom",
        "speaker": "technician",
        "dialogue": (
            "Sir, pehle actual symptom, alarm indication aur machine status "
            "note karunga."
        ),
        "visual": "Show the technician observing the equipment indicators.",
    },
    {
        "purpose": "Step 2: Review documentation",
        "speaker": "engineer",
        "dialogue": (
            "Equipment manual, approved electrical drawing aur fault history "
            "se initial checks confirm karein."
        ),
        "visual": "Show the engineer reviewing equipment documentation.",
    },
    {
        "purpose": "Step 3: Verify control",
        "speaker": "technician",
        "dialogue": (
            "Phir command, control supply aur interlock status ko "
            "approved procedure ke according verify karunga."
        ),
        "visual": "Show a safe control panel inspection.",
    },
    {
        "purpose": "Step 4: Identify the cause",
        "speaker": "engineer",
        "dialogue": (
            "Har test ko record karein. Safety devices bypass na karein "
            "aur unsupported fault assumptions se bachein."
        ),
        "visual": "Show the engineer explaining a checklist.",
    },
    {
        "purpose": "Conclusion",
        "speaker": "technician",
        "dialogue": (
            "Samajh gaya sir. Evidence ke basis par fault identify karunga "
            "aur safe procedure follow karunga. Follow IGNIVOLT!"
        ),
        "visual": "Both characters face the camera beside the relevant equipment.",
    },
]


def select_template(topic):
    normalized = topic.lower()

    if re.search(r"\bvfd\b|variable frequency|drive not starting", normalized):
        return "VFD Motor Troubleshooting", VFD_SCENES

    if re.search(r"\bplc\b|programmable logic controller", normalized):
        return "PLC Troubleshooting", PLC_SCENES

    if re.search(r"\bmotor\b|motor fault|motor troubleshooting", normalized):
        return "Motor Troubleshooting", MOTOR_SCENES

    if re.search(r"\btransformer\b", normalized):
        return "Transformer Troubleshooting", TRANSFORMER_SCENES

    return "Generic Electrical Troubleshooting", GENERIC_SCENES


def build_script(topic, duration_seconds=60):
    topic = topic.strip()

    if not topic:
        raise ValueError("Topic cannot be empty.")

    if duration_seconds not in SUPPORTED_DURATIONS:
        raise ValueError(
            "Duration must be 40, 60, or 600 seconds."
        )

    template_name, template_scenes = select_template(topic)

    if duration_seconds == 40:
        scene_count = 4
    elif duration_seconds == 60:
        scene_count = 6
    else:
        scene_count = 16

    scenes = []

    for index in range(scene_count):
        source = template_scenes[index % len(template_scenes)].copy()

        # Long videos repeat the scene structure, not the exact dialogue.
        if duration_seconds == 600 and index >= len(template_scenes):
            cycle = index // len(template_scenes) + 1
            source["dialogue"] = (
                source["dialogue"]
                + f" Practical example {cycle}: actual readings aur "
                  "equipment documentation se result verify karein."
            )
            source["purpose"] = (
                source["purpose"] + f" — Practical example {cycle}"
            )

        scene_duration = duration_seconds // scene_count
        if index < duration_seconds % scene_count:
            scene_duration += 1

        scenes.append({
            "scene": index + 1,
            "purpose": source["purpose"],
            "duration_seconds": scene_duration,
            "speaker": source["speaker"],
            "dialogue": source["dialogue"],
            "visual_prompt": (
                CHARACTER_STYLE + " Topic: " + topic + ". "
                + source["visual"]
            ),
            "review_required": True,
        })

    script_text = "\n\n".join(
        f"SCENE {scene['scene']} ({scene['duration_seconds']} seconds)\n"
        f"{scene['speaker'].title()}: {scene['dialogue']}"
        for scene in scenes
    )

    dialogue_words = sum(
        len(scene["dialogue"].split()) for scene in scenes
    )

    return {
        "channel": CHANNEL,
        "topic": topic,
        "matched_topic_template": template_name,
        "video_type": (
            "Long YouTube Video"
            if duration_seconds == 600
            else "YouTube Short"
        ),
        "language": "Hindi + Hinglish",
        "aspect_ratio": "16:9" if duration_seconds == 600 else "9:16",
        "duration_seconds": duration_seconds,
        "planned_duration_seconds": sum(
            scene["duration_seconds"] for scene in scenes
        ),
        "planned_scene_count": len(scenes),
        "status": "DRAFT_REQUIRES_HUMAN_REVIEW",
        "publishing_mode": "human_approval_required",
        "voiceover_language": "Hindi + Hinglish",
        "voiceover_note": (
            "Dialogue text only. This script generator does not create "
            "audio, animation, lip-sync or a rendered video."
        ),
        "estimated_dialogue_words": dialogue_words,
        "scenes": scenes,
        "script_text": script_text,
        "important_note": (
            "Template-based draft, not AI research. Review technical details "
            "against the exact equipment manual before use. The 600-second "
            "version is a structural draft and requires substantial expansion "
            "with verified examples to fill ten minutes naturally."
        ),
}
