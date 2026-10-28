with open("docs/assets/globe.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update animToggle check
old_anim = """  var animBtn = document.getElementById('animToggle');
  if (animBtn) {
    animBtn.addEventListener('click', function() {
      motionPaused = document.documentElement.classList.contains('anim-paused');
    });
  }"""

new_anim = """  function isMotionPaused() {
    return motionPaused || document.documentElement.classList.contains('is-anim-paused');
  }

  var animBtn = document.getElementById('animToggle');
  if (animBtn) {
    animBtn.addEventListener('click', function() {
      motionPaused = document.documentElement.classList.contains('is-anim-paused');
    });
  }"""

assert old_anim in content, "old_anim not found in globe.js"
content = content.replace(old_anim, new_anim)

# 2. Update onRender rotation check
old_rot = """        // Auto-rotation when not interacting and motion is not paused
        if (!pointerInteracting && !motionPaused) {
          targetPhi += 0.003;
        }"""

new_rot = """        // Auto-rotation when not interacting and motion is not paused
        if (!pointerInteracting && !isMotionPaused()) {
          targetPhi += 0.003;
        }"""

assert old_rot in content, "old_rot not found in globe.js"
content = content.replace(old_rot, new_rot)

with open("docs/assets/globe.js", "w", encoding="utf-8") as f:
    f.write(content)

print("docs/assets/globe.js successfully patched.")

