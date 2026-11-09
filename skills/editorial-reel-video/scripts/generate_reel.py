#!/usr/bin/env python3
"""
generate_reel.py - Concept Explainer & Editorial Swiss Poster Video Generator
Takes a voice script (or pre-recorded audio), parses high-impact typographic scenes,
dynamically pairs concepts with animated technical diagrams (e.g. Tor Onion routing,
network pipelines, terminals, architecture stacks), and renders a production-ready MP4.
Zero floral decorations, 100% clean tech aesthetics, 100% free open-source tools.
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

# Color theme sequence (high-contrast, dark-mode tech & minimal styles)
THEMES = [
    {
        "name": "theme-slate",
        "bg": "#0B132B",
        "text": "#F8FAFC",
        "badge_bg": "#38BDF8",
        "badge_text": "#0B132B",
        "is_grid": False
    },
    {
        "name": "theme-grid-paper",
        "bg": "#F8FAFC",
        "text": "#0F172A",
        "badge_bg": "#790A15",
        "badge_text": "#FAF5EA",
        "is_grid": True
    },
    {
        "name": "theme-crimson",
        "bg": "#790A15",
        "text": "#FAF5EA",
        "badge_bg": "#FAF5EA",
        "badge_text": "#111111",
        "is_grid": False
    },
    {
        "name": "theme-terminal",
        "bg": "#0D1117",
        "text": "#58A6FF",
        "badge_bg": "#238636",
        "badge_text": "#FFFFFF",
        "is_grid": False
    },
    {
        "name": "theme-obsidian",
        "bg": "#0A0A0A",
        "text": "#F8FAFC",
        "badge_bg": "#38BDF8",
        "badge_text": "#0A0A0A",
        "is_grid": False
    }
]

def parse_script_into_scenes(script_text):
    """
    Parses a voice script into structured scenes.
    Words in [brackets] are marked as hero badges.
    Lines starting with # are kicker headers.
    Lines starting with @visual: specify the animated graphic component.
    """
    raw_lines = [l.strip() for l in script_text.strip().split("\n") if l.strip()]
    scenes = []
    
    current_scene = None
    theme_idx = 0

    for line in raw_lines:
        if line.startswith("---") or line.lower().startswith("scene"):
            if current_scene:
                scenes.append(current_scene)
            theme = THEMES[theme_idx % len(THEMES)]
            theme_idx += 1
            current_scene = {
                "theme": theme,
                "kicker": "",
                "lines": [],
                "badge": "",
                "subline": "",
                "visual": None
            }
            continue

        if not current_scene:
            theme = THEMES[theme_idx % len(THEMES)]
            theme_idx += 1
            current_scene = {
                "theme": theme,
                "kicker": "",
                "lines": [],
                "badge": "",
                "subline": "",
                "visual": None
            }

        # Check for directives
        if line.startswith("#"):
            current_scene["kicker"] = line.lstrip("#").strip()
        elif line.startswith("@visual:"):
            current_scene["visual"] = line.replace("@visual:", "").strip().lower()
        elif "[" in line and "]" in line:
            parts = line.split("[")
            before = parts[0].strip()
            rest = parts[1].split("]")
            badge = rest[0].strip()
            after = rest[1].strip() if len(rest) > 1 else ""
            if before:
                current_scene["lines"].append(before)
            current_scene["badge"] = badge
            if after:
                current_scene["lines"].append(after)
        else:
            current_scene["lines"].append(line)

    if current_scene:
        scenes.append(current_scene)

    # Fallback if no delimiter was used: split by sentences
    if len(scenes) <= 1 and len(raw_lines) > 2:
        scenes = []
        for i, sentence in enumerate(raw_lines):
            theme = THEMES[i % len(THEMES)]
            words = sentence.split()
            badge = ""
            lines = []
            if len(words) > 3:
                badge = words[-1].strip("!?,.")
                lines = [" ".join(words[:-1])]
            else:
                lines = [sentence]
            scenes.append({
                "theme": theme,
                "kicker": "",
                "lines": lines,
                "badge": badge,
                "subline": "",
                "visual": None
            })

    return scenes

def load_component_html(visual_name, components_dir):
    """Loads pre-built animated HTML/SVG component."""
    if not visual_name:
        return ""
    
    file_map = {
        "network_flow": "network_flow.html",
        "tor_flow": "network_flow.html",
        "pipeline": "network_flow.html",
        "terminal": "terminal_window.html",
        "code": "terminal_window.html",
        "cli": "terminal_window.html",
        "architecture_stack": "architecture_stack.html",
        "stack": "architecture_stack.html",
        "layers": "architecture_stack.html"
    }

    filename = file_map.get(visual_name, f"{visual_name}.html")
    comp_path = components_dir / filename
    if comp_path.exists():
        with open(comp_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def generate_voiceover(text, output_path, lang="hi"):
    """Generates audio voiceover via free gTTS."""
    from gtts import gTTS
    print(f"[*] Generating speech for: {text[:60]}...")
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_path)
    print(f"[+] Audio saved to {output_path}")

def get_audio_duration(audio_file):
    """Uses ffprobe to get audio duration in seconds."""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_file
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def build_html_composition(scenes, total_duration, output_html, audio_rel_path=None):
    """Builds the standalone HyperFrames-compatible HTML composition."""
    scene_duration = total_duration / max(1, len(scenes))
    components_dir = Path(__file__).parent.parent / "resources" / "components"
    
    scenes_html = ""
    for i, sc in enumerate(scenes):
        start_t = i * scene_duration
        end_t = (i + 1) * scene_duration
        theme = sc["theme"]
        
        # Grid styles
        grid_css = ""
        if theme["is_grid"]:
            grid_css = (
                "background-image: linear-gradient(rgba(0,0,0,0.06) 1.5px, transparent 1.5px), "
                "linear-gradient(90deg, rgba(0,0,0,0.06) 1.5px, transparent 1.5px); "
                "background-size: 28px 28px; background-position: -1px -1px;"
            )

        kicker_html = f'<div class="kicker">{sc["kicker"]}</div>' if sc["kicker"] else ""
        
        lines_html = ""
        for line_idx, line in enumerate(sc["lines"]):
            delay = 0.15 * line_idx
            lines_html += f'''
            <div class="mask-container">
              <div class="text-line slide-up" style="animation-delay: {delay:.2f}s;">{line}</div>
            </div>'''
            
        badge_html = ""
        if sc["badge"]:
            badge_delay = 0.15 * len(sc["lines"])
            badge_html = f'''
            <div class="mask-container">
              <div class="slide-up" style="animation-delay: {badge_delay:.2f}s;">
                <div class="badge" style="background-color: {theme['badge_bg']}; color: {theme['badge_text']};">{sc['badge']}</div>
              </div>
            </div>'''

        # Visual component embedding
        visual_content = load_component_html(sc.get("visual"), components_dir)
        has_visual = bool(visual_content)
        
        text_container_style = (
            "position: absolute; left: 70px; top: 100px; z-index: 10; max-width: 480px;"
            if has_visual else
            "position: absolute; left: 90px; top: 110px; z-index: 10; max-width: 800px;"
        )

        visual_container_html = ""
        if has_visual:
            visual_container_html = f'''
            <div class="visual-panel" style="position: absolute; right: 50px; top: 90px; width: 700px; height: 540px; z-index: 15; display: flex; align-items: center; justify-content: center;">
              {visual_content}
            </div>'''

        scenes_html += f'''
        <!-- Scene {i+1} -->
        <div class="clip {theme['name']}" data-start="{start_t:.2f}" data-end="{end_t:.2f}"
             style="position: absolute; inset: 0; background-color: {theme['bg']}; color: {theme['text']}; {grid_css} display: {'block' if i == 0 else 'none'};">
          <div style="{text_container_style}">
            {kicker_html}
            {lines_html}
            {badge_html}
          </div>
          {visual_container_html}
        </div>
        '''

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Concept Explainer Video</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&family=JetBrains+Mono:wght@600;800&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #000;
      overflow: hidden;
      font-family: 'Montserrat', -apple-system, sans-serif;
      width: 1280px;
      height: 720px;
    }}
    #app {{
      width: 1280px;
      height: 720px;
      position: relative;
      overflow: hidden;
    }}
    /* Clean Top Header Bar (No flowers) */
    .top-header-bar {{
      position: absolute;
      top: 24px;
      left: 70px;
      right: 70px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 50;
      pointer-events: none;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 8px;
    }}
    .top-header-tag {{
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0.15em;
      color: rgba(255, 255, 255, 0.5);
      text-transform: uppercase;
    }}
    .top-header-pill {{
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.1em;
      background: rgba(255, 255, 255, 0.08);
      color: #94a3b8;
      padding: 3px 10px;
      border-radius: 4px;
      text-transform: uppercase;
    }}
    .kicker {{
      font-weight: 700;
      font-size: 24px;
      text-transform: uppercase;
      letter-spacing: 0.18em;
      margin-bottom: 12px;
      opacity: 0.90;
    }}
    .text-line {{
      font-weight: 900;
      font-size: 58px;
      line-height: 1.05;
      text-transform: uppercase;
      letter-spacing: -0.015em;
      margin-bottom: 6px;
    }}
    .badge {{
      display: inline-block;
      font-weight: 900;
      font-size: 68px;
      line-height: 1.05;
      text-transform: uppercase;
      letter-spacing: -0.015em;
      padding: 4px 18px 8px 18px;
      margin-top: 8px;
      margin-bottom: 6px;
      border-radius: 0px;
    }}
    .mask-container {{
      overflow: hidden;
      display: block;
    }}
    .slide-up {{
      transform: translateY(110%);
      animation: slideUpReveal 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
    @keyframes slideUpReveal {{
      0% {{ transform: translateY(110%); opacity: 0; }}
      100% {{ transform: translateY(0%); opacity: 1; }}
    }}
  </style>
</head>
<body>
  <div id="app" data-duration="{total_duration:.2f}" data-fps="30">
    <!-- Clean Top Branding Header (Zero Flowers) -->
    <div class="top-header-bar">
      <div class="top-header-tag">• TECHNICAL DEEP DIVE</div>
      <div class="top-header-pill">CONCEPT EXPLAINER</div>
    </div>

    <!-- Scenes Container -->
    <div id="scenes">
      {scenes_html}
    </div>
  </div>

  <script>
    // Seek-safe timeline runtime
    const sceneDuration = {scene_duration:.2f};
    const clips = document.querySelectorAll('.clip');

    function seekTo(time) {{
      clips.forEach((clip, idx) => {{
        const start = parseFloat(clip.getAttribute('data-start'));
        const end = parseFloat(clip.getAttribute('data-end'));
        if (time >= start && time < end) {{
          clip.style.display = 'block';
        }} else {{
          clip.style.display = 'none';
        }}
      }});
    }}
    window.seekTo = seekTo;
  </script>
</body>
</html>
'''
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[+] HTML composition written to {output_html}")

def find_browser_executable():
    """Finds an existing Chrome, Edge, or Chromium executable."""
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
        os.path.expanduser(r"~\AppData\Local\ms-playwright\chromium-1234\chrome-win64\chrome.exe")
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def render_with_playwright(html_file, audio_file, output_mp4, duration, fps=30):
    """Renders composition frame-by-frame using Playwright and muxes audio via FFmpeg."""
    from playwright.sync_api import sync_playwright
    import tempfile
    import shutil

    temp_dir = tempfile.mkdtemp(prefix="reel_frames_")
    print(f"[*] Rendering {duration:.2f}s at {fps} fps ({int(duration * fps)} frames)...")

    browser_exe = find_browser_executable()
    launch_kwargs = {"headless": True}
    if browser_exe:
        print(f"[*] Using browser at: {browser_exe}")
        launch_kwargs["executable_path"] = browser_exe

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(**launch_kwargs)
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto(f"file:///{Path(html_file).resolve().as_posix()}")
            page.wait_for_timeout(500)

            total_frames = int(duration * fps)
            for f in range(total_frames):
                current_time = f / fps
                page.evaluate(f"window.seekTo({current_time})")
                frame_path = os.path.join(temp_dir, f"frame_{f:05d}.png")
                page.screenshot(path=frame_path)

            browser.close()

        print(f"[+] All frames captured. Compiling video with FFmpeg...")
        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", os.path.join(temp_dir, "frame_%05d.png"),
            "-i", audio_file,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-shortest",
            output_mp4
        ]
        subprocess.run(cmd, check=True)
        print(f"[✓] Final Video successfully created: {output_mp4}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    parser = argparse.ArgumentParser(description="Generate Concept Explainer Video from Script")
    parser.add_argument("--script", type=str, help="Raw script text or path to script file")
    parser.add_argument("--audio", type=str, help="Existing voiceover audio file (optional)")
    parser.add_argument("--output", type=str, default="output_reel.mp4", help="Output MP4 file name")
    parser.add_argument("--fps", type=int, default=30, help="Output framerate")
    parser.add_argument("--lang", type=str, default="hi", help="Language code for TTS (default: hi)")
    args = parser.parse_args()

    if not args.script and not args.audio:
        print("Error: Please provide --script or --audio")
        sys.exit(1)

    script_text = args.script or ""
    if os.path.exists(script_text):
        with open(script_text, "r", encoding="utf-8") as f:
            script_text = f.read()

    audio_file = args.audio
    if not audio_file:
        audio_file = "voiceover_temp.mp3"
        clean_text = ""
        for line in script_text.splitlines():
            if not line.startswith("@") and not line.startswith("---"):
                clean_text += line.replace("[", "").replace("]", "").replace("#", "") + " "
        generate_voiceover(clean_text, audio_file, lang=args.lang)

    duration = get_audio_duration(audio_file)
    print(f"[*] Audio duration: {duration:.2f}s")

    scenes = parse_script_into_scenes(script_text)
    print(f"[*] Parsed {len(scenes)} scenes.")

    html_file = "composition.html"
    build_html_composition(scenes, duration, html_file, audio_rel_path=audio_file)

    render_with_playwright(html_file, audio_file, args.output, duration, fps=args.fps)

if __name__ == "__main__":
    main()
