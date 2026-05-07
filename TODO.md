
- [ ] Inspect current speech flow (frontend vs backend) to locate duplicate TTS calls
- [x] Found duplication: backend /command route can call speak(), while frontend also calls speak() on response
- [x] Remove backend speak() calls from backend/app/main.py /command route and return strings instead
- [x] Ensure frontend continues to be the only place that calls JarvisAPI.speak()

- [x] Run app and verify single utterance per entered command

