/* =========================================================================
   VOICE CHAT WIDGET — push-to-talk
   Add these script tags at the end of index.html, after your existing
   script tags (the VAD/onnxruntime tags are no longer needed):

     <script src="voice-widget.js"></script>

   How it works:
   - Press and HOLD the orb -> mic opens, recording starts
   - Release the orb -> recording stops, the clip gets sent to your backend
   - The reply is read aloud (Web Speech Synthesis, free, built into the
     browser)
   - The orb's visual state reflects idle / recording / thinking / speaking

   Two things to wire up to your own backend:
   1. TRANSCRIBE_ENDPOINT — where the recorded audio clip gets POSTed
   2. getAIReply(text) — only needed if /transcribe returns just the raw
      transcript; skip it if your endpoint already returns the AI's reply
      (see the note inside sendAudioToBackend())
   ========================================================================= */
let sessionId = null;

(function () {
  const fab = document.getElementById("voiceFab");
  const overlay = document.getElementById("voiceModalOverlay");
  const closeBtn = document.getElementById("voiceModalClose");
  const orbWrap = document.querySelector(".orb-wrap");
  const orbBtn = document.getElementById("orbBtn");
  const statusEl = document.getElementById("voiceStatus");
  const conversationEl = document.getElementById("voiceConversation");
  const conversationEmptyEl = document.getElementById("voiceConversationEmpty");

  const supportsRecording = !!(navigator.mediaDevices && window.MediaRecorder);

  let mediaStream = null; // requested once, reused across presses
  let mediaRecorder = null;
  let chunks = [];
  let isRecording = false;

  // Change this to your real backend URL when you deploy
  // (localhost only works while you're testing on your own machine).
  const TRANSCRIBE_ENDPOINT = "/api/voice/AI-agent/chat";

  // Set to true while testing locally to also download each clip so you
  // can listen back to exactly what got sent. Turn off before you deploy.
  const DEBUG_DOWNLOAD_RECORDING = false;

  /* ----------------------------------------------------------------------
     PLACEHOLDER — replace this with your real backend call for the AI's
     reply. It must return a Promise that resolves to a string.
     If your /transcribe endpoint already returns the AI's reply (not just
     the raw transcript), you can skip this and use that text directly —
     see the note inside sendAudioToBackend().
     ---------------------------------------------------------------------- */

  // ---------------------------------------------------------------------
  // Modal open / close
  // ---------------------------------------------------------------------
  function openModal() {
    overlay.classList.add("open");
    document.body.style.overflow = "hidden";
  }
  function closeModal() {
    overlay.classList.remove("open");
    document.body.style.overflow = "";
    window.speechSynthesis?.cancel();
    if (isRecording) stopRecording();
    releaseMic();
    setState(null);
    setStatus("Hold the orb to talk");
  }

  fab.addEventListener("click", openModal);
  closeBtn.addEventListener("click", closeModal);
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) closeModal();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && overlay.classList.contains("open")) closeModal();
  });

  // ---------------------------------------------------------------------
  // Orb visual states
  // ---------------------------------------------------------------------
  function setState(state) {
    orbWrap.classList.remove("is-listening", "is-thinking", "is-speaking", "is-error");
    if (state) orbWrap.classList.add(state);
  }
  function setStatus(text) {
    statusEl.textContent = text;
  }

  // ---------------------------------------------------------------------
  // Mic setup — requested once on first press, reused after that so the
  // permission prompt only ever appears one time per visit.
  // ---------------------------------------------------------------------
  async function ensureMic() {
    if (mediaStream) return true;
    try {
      mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: false,
          noiseSuppression: false,
          autoGainControl: false,
          channelCount: 1,
          sampleRate: 48000,
        },
      });
      return true;
    } catch (err) {
      setState("is-error");
      setStatus("Mic access denied — allow microphone access and try again");
      setTimeout(() => setState(null), 2000);
      return false;
    }
  }

  function releaseMic() {
    if (mediaStream) {
      mediaStream.getTracks().forEach((t) => t.stop());
      mediaStream = null;
    }
  }

  // ---------------------------------------------------------------------
  // Push-to-talk recording: start on press, stop on release
  // ---------------------------------------------------------------------
  async function startRecording() {
    if (isRecording) return;
    if (!supportsRecording) {
      setStatus("Voice input isn't available in this browser");
      return;
    }

    window.speechSynthesis?.cancel();

    const ok = await ensureMic();
    if (!ok) return;

    mediaRecorder = new MediaRecorder(mediaStream, { audioBitsPerSecond: 256000 });
    chunks = [];

    mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
    mediaRecorder.onstop = () => {
      const blob = new Blob(chunks, { type: mediaRecorder.mimeType });
      chunks = [];

      if (DEBUG_DOWNLOAD_RECORDING) downloadAudio(blob, mediaRecorder.mimeType);

      sendAudioToBackend(blob);
    };

    mediaRecorder.start();
    isRecording = true;
    setState("is-listening");
    setStatus("Recording… release to send");
  }

  function stopRecording() {
    if (!isRecording) return;
    isRecording = false;
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.stop(); // onstop fires -> builds blob -> sends it
      setState("is-thinking");
      setStatus("Thinking…");

      // Disable recording button
      orbBtn.style.pointerEvents = "none";
      orbBtn.style.opacity = "0.6";
    } else {
      setState(null);
      setStatus("Hold the orb to talk");
    }
  }

  // ---------------------------------------------------------------------
  // ---------------------------------------------------------------------
  async function sendAudioToBackend(blob) {
    const ext = (mediaRecorder.mimeType.split("/")[1] || "webm").split(";")[0];

    try {
      const formData = new FormData();
      formData.append("audio", blob, `recording.${ext}`);

      if (sessionId) {
        formData.append("session_id", sessionId);
    }

      const response = await fetch(TRANSCRIBE_ENDPOINT, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error(`Server responded ${response.status}`);

      const result = await response.json();
      
      // 1. Session ID 
      sessionId = result.session_id;
      
      // 2. User said
      const said = result.transcript || "";

      // 3. AI Response text
      const textResponse = result.answer || "";

      // 3. AI Response Audio bytes
      let audio_url = null;
        if (result.audio_base64) {
            const cleanBase64 = result.audio_base64.replace(/\s/g, '');
            audio_url = `data:audio/wav;base64,${cleanBase64}`;
        }

      // 5. Display and play Response
      displayTranscript(said, textResponse, audio_url);

    } 
    catch (err) {
      console.error("Transcription error:", err);
      setState("is-error");
      setStatus("Couldn't reach the server — check your connection and try again");

      // Enable recording button
      orbBtn.style.pointerEvents = "auto";
      orbBtn.style.opacity = "1";
      setTimeout(() => setState(null), 2200);
    }
  }

  // ---------------------------------------------------------------------
  // Conversation log — renders each turn as a user bubble + AI bubble
  // ---------------------------------------------------------------------
  function addBubble(role, text) {
    if (conversationEmptyEl) conversationEmptyEl.remove();

    const bubble = document.createElement("div");
    bubble.className = `voice-bubble voice-bubble-${role === "user" ? "user" : "ai"}`;

    const label = document.createElement("span");
    label.className = "voice-bubble-label";
    label.textContent = role === "user" ? "You" : "Youssef AI";

    const body = document.createElement("span");
    body.textContent = text;

    bubble.appendChild(label);
    bubble.appendChild(body);
    conversationEl.appendChild(bubble);
    conversationEl.scrollTop = conversationEl.scrollHeight;
    return bubble;
  }

  // ---------------------------------------------------------------------
  // Sending the message and speaking the reply
  // ---------------------------------------------------------------------
  async function displayTranscript(transcript, answer, audio_url) {
    try {
      if (transcript) addBubble("user", transcript);
      addBubble("ai", answer);
      playReply(audio_url);

    } catch (err) {
      console.error("Voice widget error:", err);
      setState("is-error");
      setStatus("Something went wrong — try again");
      setTimeout(() => setState(null), 2000);
    }
}

function playReply(audio_url) {
    if (!audio_url) {
        setState(null);
        setStatus("Hold the orb to ask something else");

        // Enable recording button
        orbBtn.style.pointerEvents = "auto";
        orbBtn.style.opacity = "1";
        return;
    }

    const audio = new Audio(audio_url);

    audio.onplay = () => {
      setState("is-speaking");
      setStatus("Speaking...");
    };

    audio.onerror = () => {
      setState("is-error");
      setStatus("Couldn't play audio");
    };

    audio.onended = () => {
      setState(null);
      setStatus("Hold the orb to ask something else");

      // Enable recording button
        orbBtn.style.pointerEvents = "auto";
        orbBtn.style.opacity = "1";
    };

    audio.play().catch(err => {
        console.error("Audio play failed:", err);
        setState("is-error");
        setStatus("Playback blocked or failed");

        // Enable recording button
        orbBtn.style.pointerEvents = "auto";
        orbBtn.style.opacity = "1";
    });
}

  // ---------------------------------------------------------------------
  // Wiring: press-and-hold on the orb (mouse + touch), typed fallback
  // ---------------------------------------------------------------------
  orbBtn.addEventListener("mousedown", startRecording);
  orbBtn.addEventListener("mouseup", stopRecording);
  orbBtn.addEventListener("mouseleave", () => { if (isRecording) stopRecording(); });

  orbBtn.addEventListener("touchstart", (e) => { e.preventDefault(); startRecording(); }, { passive: false });
  orbBtn.addEventListener("touchend", (e) => { e.preventDefault(); stopRecording(); }, { passive: false });
  orbBtn.addEventListener("touchcancel", (e) => { e.preventDefault(); if (isRecording) stopRecording(); });

  if (!supportsRecording) {
    setStatus("Voice input isn't available in this browser");
  } else {
    setStatus("Hold the orb to talk");
  }
})();

// ---------------------------------------------------------------------
// Debug helper — downloads the exact clip that gets sent to the backend,
// so you can listen back and confirm recording quality. Controlled by
// DEBUG_DOWNLOAD_RECORDING above; turn that off before deploying.
// ---------------------------------------------------------------------
function downloadAudio(blob, mimeType) {
  const ext = (mimeType.split("/")[1] || "webm").split(";")[0];
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `recording.${ext}`;
  a.click();
  URL.revokeObjectURL(url);
}