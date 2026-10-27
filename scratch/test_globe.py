from playwright.sync_api import sync_playwright

test_html = """<!DOCTYPE html>
<html>
<head>
<style>
body { margin: 0; background: #0b0f19; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
.globe-wrap { width: 360px; height: 360px; position: relative; }
canvas { width: 100%; height: 100%; }
</style>
</head>
<body>
<div class="globe-wrap">
  <canvas id="cobe" width="720" height="720"></canvas>
</div>
<script type="module">
import createGlobe from './docs/assets/cobe.js';

const canvas = document.getElementById('cobe');
let phi = 1.35;
let theta = 0.25;

try {
  const globe = createGlobe(canvas, {
    devicePixelRatio: 2,
    width: 720,
    height: 720,
    phi: 1.35,
    theta: 0.25,
    dark: 1,
    diffuse: 1.2,
    mapSamples: 16000,
    mapBrightness: 6,
    baseColor: [0.3, 0.35, 0.45],
    markerColor: [0.1, 0.8, 1],
    glowColor: [0.2, 0.3, 0.5],
    markers: [
      { location: [12.9716, 77.5946], size: 0.08 }
    ],
    onRender: (state) => {
      state.phi = phi;
      state.theta = theta;
      phi += 0.003;
    }
  });
  window.__globe_initialized = true;
  console.log('Globe created successfully!');
} catch (e) {
  console.error('Error creating globe:', e);
}
</script>
</body>
</html>
"""

open("scratch/test_globe.html", "w", encoding="utf-8").write(test_html)

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    logs = []
    errors = []
    page.on("console", lambda msg: logs.append(msg.text) if msg.type != "error" else errors.append(msg.text))
    page.on("pageerror", lambda err: errors.append(str(err)))
    
    page.goto("http://localhost:8000/test_globe.html", wait_until="networkidle")
    page.wait_for_timeout(2000)
    
    ok = page.evaluate("() => window.__globe_initialized")
    print("Logs:", logs)
    print("Errors:", errors)
    print("Globe Initialized:", ok)
    
    # Take screenshot of the rendered globe!
    page.screenshot(path="scratch/globe_screenshot.png")
    print("Saved screenshot to scratch/globe_screenshot.png")
    b.close()
