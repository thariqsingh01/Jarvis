// renderer.js

const log = document.getElementById("log");
const input = document.getElementById("commandInput");
const sendBtn = document.getElementById("sendBtn");
const listenBtn = document.getElementById("listenBtn");
const animationContainer = document.getElementById("jarvis-animation");

// ----------------------------
// Initialize Lottie Animation
// ----------------------------
let animation;
try {
  animation = lottie.loadAnimation({
    container: animationContainer,
    renderer: 'svg',
    loop: true,
    autoplay: false,
    path: 'jarvis.json' // make sure this file exists in electron/
  });
} catch (err) {
  console.warn("Lottie failed to load:", err);
}

// ----------------------------
// Utility: Update Log
// ----------------------------
function updateLog(text) {
  log.innerHTML += text + "<br>";
  log.scrollTop = log.scrollHeight; // scroll to bottom
}

// ----------------------------
// Send Typed Command
// ----------------------------
sendBtn.addEventListener("click", async () => {
  const cmd = input.value.trim();
  if (!cmd) return;

  updateLog(`You: ${cmd}`);
  input.value = "";

  try {
    const response = await window.JarvisAPI.command(cmd);

    if (response.shutdown) {
      updateLog("Jarvis: Shutting down backend.");
      if (animation) animation.stop();
      await window.JarvisAPI.speak("Goodbye!");
      return;
    }

    if (response.response) {
      updateLog(`Jarvis: ${response.response}`);
      await window.JarvisAPI.speak(response.response);
    }
  } catch (err) {
    updateLog("Error sending command: " + err.message);
  }
});

// ----------------------------
// Listen Button
// ----------------------------
listenBtn.addEventListener("click", async () => {
  updateLog("Listening...");
  listenBtn.disabled = true;

  if (animation) animation.play();

  let commandText = "";
  try {
    const response = await window.JarvisAPI.listen();
    commandText = response.command || "";
  } catch (err) {
    updateLog("Microphone error: " + err.message);
  }

  if (animation) animation.stop();

  if (!commandText) {
    updateLog("No command detected.");
    listenBtn.disabled = false;
    return;
  }

  updateLog(`You: ${commandText}`);

  try {
    const cmdResponse = await window.JarvisAPI.command(commandText);

    if (cmdResponse.shutdown) {
      updateLog("Jarvis: Shutting down backend.");
      await window.JarvisAPI.speak("Goodbye!");
      return;
    }

    if (cmdResponse.response) {
      updateLog(`Jarvis: ${cmdResponse.response}`);
      await window.JarvisAPI.speak(cmdResponse.response);
    }
  } catch (err) {
    updateLog("Error processing command: " + err.message);
  }

  listenBtn.disabled = false;
});

