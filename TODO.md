# Reverted Voice Fix Changes

All changes reverted to original state:
- backend/app/voice.py: Original timeouts/logging/mic_index
- backend/app/main.py: Original /listen without device_index or list_mics
- electron/renderer.js: Original button behavior
- Removed TODO.md

App restored. Original issue persists, but per request.
