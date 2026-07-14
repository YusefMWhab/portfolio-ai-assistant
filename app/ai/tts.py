from app.ai.providers.gemini_provider import GeminiProvider
import io
import wave
import base64
import edge_tts
import re
import asyncio
import json


class TextToSpeech:

    def __init__(self):

        self.gemini = GeminiProvider()

    def split_text(self, text: str, max_chars: int = 100):

        sentences = re.split(
            r'(?<=[.!؟!])\s+|\n\n+',
            text
        )

        chunks = []

        current = ""

        for sentence in sentences:

            if len(current) + len(sentence) <= max_chars:
                current += " " + sentence

            else:
                if current.strip():
                    chunks.append(
                        current.strip()
                    )

                current = sentence

        if current.strip():
            chunks.append(
                current.strip()
            )

        return chunks

    async def generateAudio(self, text: str, language) -> str:
       

        """    raw_pcm_bytes = await self.gemini.text_to_speech(text)
        
        # 2. السحر كله هنا: تحويل الـ Raw PCM لـ WAV سليم بالهيدرز بتاعته في الميموري
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wav_file:
            # إعدادات الصوت الافتراضية لـ Gemini (Monoral, 2-bytes per sample, 24000Hz)
            wav_file.setnchannels(1)      # Mono
            wav_file.setsampwidth(2)      # 16-bit
            wav_file.setframerate(24000)  # 24kHz معدل ترميز جمناي المشهور
            wav_file.writeframes(raw_pcm_bytes)
            
        # 3. بناخد الـ wav الكامل بالهيدر بتاعه
        full_wav_bytes = wav_buffer.getvalue()
        
        # 4. بنحوله لـ Base64 String ونرجعه
        audio_base64_str = base64.b64encode(full_wav_bytes).decode('utf-8')
        
        return audio_base64_str 
        """ 

        text = re.sub(re.compile(r'\*+'), '', text)
        
        text = re.sub(re.compile(r'#+\s*'), '', text)
        
        text = re.sub(re.compile(r'^\s*[-*+]\s+', re.MULTILINE), '', text)
        
        text = text.replace('\n', ' ').replace('\r', ' ')
        
        text = re.sub(re.compile(r'\s+'), ' ', text).strip()
        
        if not text:
            return ""

        try:
            lang_str = str(language).lower()

            if "ar" in lang_str:
                voice = "ar-EG-ShakirNeural"
                current_rate = "+5%"
            else:
                voice = "en-US-BrianNeural"
                current_rate = "+15%"

            communicate = edge_tts.Communicate(text, voice, rate=current_rate)
            
            audio_bytes = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_bytes += chunk["data"]
            
            audio_base64_str = base64.b64encode(audio_bytes).decode('utf-8')
            return audio_base64_str
            
        except Exception as e:
            print(f"Edge TTS Error: {str(e)}")
            raise e
        
    async def generateStream(self, fullAnswer: str, language):

        chunks = self.split_text(fullAnswer)

        for chunk in chunks:


            audio_base64_str = await self.generateAudio(
                    chunk,
                    language
                )

            if not audio_base64_str:
                continue

            yield json.dumps({"audio_base64": audio_base64_str}) + "\n"