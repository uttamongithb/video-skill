# HyperFrames Authoring Specification for Editorial Reels

This guide details how to construct renderable HyperFrames HTML compositions matching the Editorial Swiss Typography format.

---

## 1. Composition Structure & Data Attributes
HyperFrames requires:
- `<div id="app">` root container with `data-duration="<seconds>"` and `data-fps="30"`.
- Scenes authored as `<div class="clip" data-start="<start_s>" data-end="<end_s>">`.
- Synchronized audio tracks via `<audio src="audio.mp3" data-start="0"></audio>`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="resources/grid_pattern.css">
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
</head>
<body style="margin: 0; padding: 0; background: #000; overflow: hidden;">
  <div id="app" data-duration="31.55" data-fps="30" style="width: 1280px; height: 720px; position: relative;">

    <!-- Background Music -->
    <audio src="bgm.mp3" data-start="0" data-volume="0.18"></audio>
    <!-- Voiceover -->
    <audio src="voiceover.mp3" data-start="0" data-volume="1.0"></audio>

    <!-- Sakura Corner Ornaments (Persistent Layer) -->
    <div style="position: absolute; top: 12px; left: 16px; z-index: 100; pointer-events: none;">
      <img src="resources/sakura_corner.svg" width="130" height="130">
    </div>
    <div style="position: absolute; top: 12px; right: 16px; transform: scaleX(-1); z-index: 100; pointer-events: none;">
      <img src="resources/sakura_corner.svg" width="130" height="130">
    </div>

    <!-- Scene 1: Problem Hook -->
    <div class="clip theme-crimson" data-start="0" data-end="3.27" style="position: absolute; inset: 0;">
      <div style="position: absolute; left: 90px; top: 80px; z-index: 10;">
        <div class="mask-container"><div class="text-line slide-up">HAR</div></div>
        <div class="mask-container"><div class="text-line slide-up" style="animation-delay: 0.25s;">COMPANY</div></div>
        <div class="mask-container"><div class="text-line slide-up" style="animation-delay: 0.65s;">MEIN SAME</div></div>
        <div class="mask-container">
          <div class="slide-up" style="animation-delay: 1.1s;">
            <div class="badge-cream text-line" style="font-size: 78px; margin-top: 10px;">RESUME</div>
          </div>
        </div>
        <div class="mask-container"><div class="text-line slide-up" style="font-size: 42px; animation-delay: 1.6s; opacity: 0.9;">BHEJ RAHE HO?</div></div>
      </div>
      <!-- Character Avatar -->
      <img src="avatars/avatar_talk.png" style="position: absolute; right: 70px; bottom: 0px; height: 500px; z-index: 5;">
    </div>

    <!-- Scene 2: Grid Milestone -->
    <div class="clip theme-grid-paper" data-start="8.43" data-end="12.0" style="position: absolute; inset: 0;">
      <div style="position: absolute; left: 90px; top: 75px; z-index: 10;">
        <div class="kicker">AAJ HAI</div>
        <div style="display: flex; align-items: center; gap: 18px;">
          <div class="text-line" style="font-size: 140px; margin: 0;">DAY</div>
          <div class="badge-crimson" style="font-size: 140px; line-height: 1; padding: 0 22px;">15</div>
        </div>
        <div class="kicker" style="font-size: 38px; margin-top: 18px; letter-spacing: 0.08em;">OF AI FOR COLLEGE</div>
      </div>
      <img src="avatars/avatar_thumbsup.png" style="position: absolute; right: 70px; bottom: 0px; height: 500px; z-index: 5;">
    </div>

    <!-- Scene 3: App Mockup Demo -->
    <div class="clip theme-studio" data-start="17.5" data-end="22.7" style="position: absolute; inset: 0;">
      <!-- Device Mockup Window -->
      <div style="position: absolute; left: 340px; top: 70px; width: 860px; height: 490px; border-radius: 20px; overflow: hidden; box-shadow: 0 24px 60px rgba(0,0,0,0.35); border: 8px solid #222;">
        <video src="app_demo.mp4" data-start="17.5" style="width: 100%; height: 100%; object-fit: cover;"></video>
      </div>
      <!-- Side Captions -->
      <div style="position: absolute; left: 80px; top: 90px; z-index: 10;">
        <div class="text-line" style="font-size: 52px;">JOB</div>
        <div><span class="badge-cream text-line" style="font-size: 44px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">DESCRIPTION</span></div>
        <div class="text-line" style="font-size: 52px;">PASTE</div>
        <div><span class="badge-crimson text-line" style="font-size: 48px;">KARO,</span></div>
      </div>
      <!-- Bottom Caption Bar -->
      <div style="position: absolute; left: 340px; bottom: 40px; z-index: 10;">
        <div class="kicker" style="font-size: 24px;">AUR YE TUMHARE</div>
        <div style="display: flex; align-items: center; gap: 12px;">
          <span class="badge-crimson text-line" style="font-size: 42px;">RESUME</span>
          <span class="text-line" style="font-size: 42px;">KO US JOB KE ACCORDING</span>
          <span class="badge-crimson text-line" style="font-size: 42px;">TAILOR</span>
        </div>
      </div>
    </div>

    <!-- Scene 4: Outro CTA -->
    <div class="clip theme-black" data-start="29.33" data-end="31.55" style="position: absolute; inset: 0;">
      <div style="position: absolute; left: 90px; top: 90px; z-index: 10;">
        <div class="kicker">KE LIYE</div>
        <div><span class="badge-crimson text-line" style="font-size: 110px;">FOLLOW</span></div>
        <div class="text-line" style="font-size: 80px; margin-top: 10px;">KAR LENA!</div>
      </div>
      <img src="avatars/avatar_heart.png" style="position: absolute; right: 70px; bottom: 0px; height: 500px; z-index: 5;">
    </div>

  </div>
</body>
</html>
```

---

## 2. Rendering with HyperFrames CLI
To validate and render:
```bash
# 1. Check composition syntax and runtime
npx hyperframes check

# 2. Render MP4 output
npx hyperframes render -o output_video.mp4 --fps 30
```
HyperFrames will automatically use the local Chrome/Chromium and FFmpeg build to render frame-by-frame with deterministic synchronization.
