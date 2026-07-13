from app.ai.providers.gemini_provider import GeminiProvider
import io
import wave
import base64
import edge_tts
import re


class TextToSpeech:

    def __init__(self):

        self.gemini = GeminiProvider()

    async def generateAudio(self, text: str, language) -> str:
       

        """ raw_pcm_bytes = await self.gemini.text_to_speech(text)
        
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
        
        return audio_base64_str  """

        # 1. إزالة نجوم المارك داون (Bold/Italic) مثل **text** أو *text*
        text = re.sub(re.compile(r'\*+'), '', text)
        
        # 2. إزالة علامات العناوين مثل ### أو ##
        text = re.sub(re.compile(r'#+\s*'), '', text)
        
        # 3. إزالة الشرط بتاعة الـ Bullet points في أول السطور
        text = re.sub(re.compile(r'^\s*[-*+]\s+', re.MULTILINE), '', text)
        
        # 4. استبدال السطور الجديدة بمسافات عشان الكلام يتدفق ورا بعضه وميقفش كتير
        text = text.replace('\n', ' ').replace('\r', ' ')
        
        # 5. تنظيف المسافات الزيادة
        text = re.sub(re.compile(r'\s+'), ' ', text).strip()
        
        if not text:
            return ""

        try:
            # تحويل الـ language لـ string وتوحيد شكلها عشان الأمان
            lang_str = str(language).lower()

            # تشيك مرن: بيقبل لو جاي "ar" أو "arabic" أو "language.arabic"
            if "ar" in lang_str:
                voice = "ar-EG-ShakirNeural"
                current_rate = "+5%"
            else:
                voice = "en-US-BrianNeural"
                current_rate = "+15%"

            # إرسال النص المتنظف مع ريت أسرع 15% للإنجاز
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