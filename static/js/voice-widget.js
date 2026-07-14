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

  // Streaming-audio playback queue: chunks arrive over time from the
  // server, we play them back-to-back instead of firing them all at once.
  let audioQueue = [];
  let isPlayingAudio = false;
  let sessionLimitReached = false;

  function lockOrb() {
    orbBtn.style.pointerEvents = "none";
    orbBtn.style.opacity = "0.5";
  }
  function unlockOrb() {
    if (sessionLimitReached) return; // stay locked once the limit is hit
    orbBtn.style.pointerEvents = "auto";
    orbBtn.style.opacity = "1";
  }

  // End-Points
  const TRANSCRIBE_ENDPOINT = "/api/voice/AI-agent/chat";
  const AUDIO_GET_ENDPOINT = "/api/voice/AI-agent/audio-stream/"



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
    audioQueue = [];
    isPlayingAudio = false;
    unlockOrb();
    setState(null);
  }

  // Tells the backend to drop this session's data right away instead of
  // waiting for it to idle out. Uses sendBeacon so it still fires even
  // as the page/tab is closing (a normal fetch can get cancelled then).
  function endSessionOnServer() {
    if (!sessionId) return;
    const url = `/api/voice/AI-agent/end-session/${sessionId}`;

    if (navigator.sendBeacon) {
      navigator.sendBeacon(url, new Blob([], { type: "application/json" }));
    } else {
      fetch(url, { method: "POST", keepalive: true }).catch(() => { });
    }

    sessionId = null;
    sessionLimitReached = false;
    orbBtn.style.pointerEvents = "auto";
    orbBtn.style.opacity = "1";
  }

  // Catches the case where the user closes the whole tab/browser
  // without explicitly closing the widget first.
  window.addEventListener("pagehide", endSessionOnServer);

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
    if (sessionLimitReached) {
      setStatus("You've reached this conversation's question limit");
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
    } else {
      setState(null);
      setStatus("Hold the orb to talk");
    }
  }

  // ---------------------------------------------------------------------
  // Sending the recorded clip to your transcription/AI backend
  // ---------------------------------------------------------------------
  async function sendAudioToBackend(blob) {
    const ext = (mediaRecorder.mimeType.split("/")[1] || "webm").split(";")[0];
    lockOrb();

    audioQueue = [];

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
      if (!response.ok) {
        const error = await response.json();
        displaySystemMessage(error.detail.message);
        throw new Error(error.detail.error);
        unlockOrb();
      }


      const result = await response.json();

      sessionId = result.session_id;

      const said = result.transcription || "";
      const textResponse = result.answer || "";

      // Show the text turn right away…
      displayTranscript(said, textResponse);

      // …then stream and play the AI's spoken reply as it arrives.
      setState("is-thinking");
      setStatus("Thinking…");
      await streamAudio(sessionId);

      if (sessionLimitReached) {
        setStatus("You've reached this conversation's question limit");
      }

      const remaining_questions = result.remaining_questions || 0;
      if (remaining_questions > 0) {
        sessionLimitReached = false;
      }
      else {
        sessionLimitReached = true;
      }

    } catch (err) {
      console.error("Transcription error:", err);
      setState("is-error");
      setStatus("Couldn't reach the server — check your connection and try again");
      unlockOrb();
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
  // Display the transcript + AI text turn (audio is handled separately
  // by streamAudio/playNextAudio below)
  // ---------------------------------------------------------------------
  function displayTranscript(transcript, answer) {
    try {
      if (transcript) addBubble("user", transcript);
      addBubble("ai", answer);
    } catch (err) {
      console.error("Voice widget error:", err);
      setState("is-error");
      setStatus("Something went wrong — try again");
      setTimeout(() => setState(null), 2000);
    }
  }

  // ---------------------------------------------------------------------
  // ---------------------------------------------------------------------
  async function streamAudio(sessionId) {
    const response = await fetch(`${AUDIO_GET_ENDPOINT}${sessionId}`);

    if (!response.ok) {
      unlockOrb();
        const error = await response.json();
        displaySystemMessage(error.detail.message);
        throw new Error("Audio stream failed")
      }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    let gotAnyValidChunk = false;

    while (true) {
      const { done, value } = await reader.read();

      if (value) {
        buffer += decoder.decode(value, { stream: true });

        let newlineIndex;
        while ((newlineIndex = buffer.indexOf("\n")) !== -1) {
          const line = buffer.slice(0, newlineIndex).trim();
          buffer = buffer.slice(newlineIndex + 1);
          if (line && tryEnqueueNdjsonLine(line)) gotAnyValidChunk = true;
        }
      }

      if (done) {
        const leftover = buffer.trim();
        if (leftover) {
          if (tryEnqueueNdjsonLine(leftover)) gotAnyValidChunk = true;
          else if (!gotAnyValidChunk) enqueueBase64Audio(buffer);
        }
        break;
      }
    }
  }

  // Tries to parse one line as {"audio_base64": "..."} and queue it.
  // Returns true if it was valid NDJSON, false otherwise.
  function tryEnqueueNdjsonLine(line) {
    try {
      const { audio_base64 } = JSON.parse(line);
      if (!audio_base64) return false;
      enqueueBase64Audio(audio_base64);
      return true;
    } catch {
      return false;
    }
  }

  // Decodes a base64 MP3 string into a playable data: URI and queues it.
  function enqueueBase64Audio(audio_base64) {
    if (!audio_base64) return;
    const cleanBase64 = audio_base64.replace(/\s/g, "");
    if (!cleanBase64) return;

    const url = `data:audio/mpeg;base64,${cleanBase64}`;
    audioQueue.push(url);
    playNextAudio(); // no-op if something's already playing — it'll pick this up next
  }

  // ---------------------------------------------------------------------
  // Plays queued audio chunks back-to-back, one at a time. Safe to call
  // repeatedly — it's a no-op while something is already playing.
  // ---------------------------------------------------------------------
  function playNextAudio() {
    if (isPlayingAudio) return;

    if (audioQueue.length === 0) {
      setState(null);
      setStatus(sessionLimitReached ? "You've reached this conversation's question limit" : "Hold the orb to ask something else");
      unlockOrb();
      return;
    }

    const url = audioQueue.shift();
    isPlayingAudio = true;

    const audio = new Audio(url);

    audio.onplay = () => {
      setState("is-speaking");
      setStatus("Speaking...");
    };

    audio.onerror = () => {
      isPlayingAudio = false;
      setState("is-error");
      setStatus("Couldn't play audio");
      unlockOrb();
    };

    audio.onended = () => {
      isPlayingAudio = false;
      playNextAudio(); // move on to the next queued chunk, if any
    };

    audio.play().catch((err) => {
      console.error("Audio play failed:", err);
      isPlayingAudio = false;
      setState("is-error");
      setStatus("Playback blocked or failed");
      unlockOrb();
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

function displaySystemMessage(message) {
  displayTranscript("", message);
}
