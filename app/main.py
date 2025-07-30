import os
import speech_recognition as sr 
import pyttsx3
from langgraph.checkpoint.mongodb import MongoDBSaver
from .graph import create_chat_graph


MONGODB_URI = "mongodb://localhost:27017"
config = {"configurable": {"thread_id": "60"}}

def text_to_speech(text, rate=200, volume=0.9, voice_gender='female'):
    """
    Convert text to speech
    """
    if not text or not text.strip():
        print("No text provided for TTS")
        return False
        
    try:
        # Initialize TTS engine
        tts_engine = pyttsx3.init()
        
        # Set speech rate
        tts_engine.setProperty('rate', rate)
        
        # Set volume
        tts_engine.setProperty('volume', volume)
        
        # Voice gender select
        voices = tts_engine.getProperty('voices')
        if voices:
            if voice_gender.lower() == 'male' and len(voices) > 0:
                tts_engine.setProperty('voice', voices[0].id)
            elif voice_gender.lower() == 'female' and len(voices) > 1:
                tts_engine.setProperty('voice', voices[1].id)
        
        # text bolne ke liye hai
        tts_engine.say(text.strip())
        tts_engine.runAndWait()
        
        return True
        
    except Exception as e:
        print(f"TTS Error: {e}")
        return False

def main():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph = create_chat_graph(checkpointer=checkpointer)
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 2

            while True:
                try:
                    print("Say something!")
                    audio = r.listen(source)
                    
                    print("Processing audio...")
                    sst = r.recognize_google(audio)
                    
                    if not sst or not sst.strip():
                        print("Empty speech input detected, skipping...")
                        continue
                    
                    print("You said:", sst)
                    
                    response_text = ""
                    for event in graph.stream({"messages": [{"role": "user", "content": sst.strip()}]}, config, stream_mode="values"):
                        if "messages" in event and event["messages"]:
                            last_message = event["messages"][-1]
                            last_message.pretty_print()
                            
                            # Safely extract content
                            if hasattr(last_message, 'content') and last_message.content:
                                response_text = str(last_message.content).strip()
                    
                    # Convert AI response to speech
                    if response_text:
                        print("AI Response:", response_text)
                        text_to_speech(response_text)
                    else:
                        fallback_msg = "I didn't receive a response. Please try again."
                        print(fallback_msg)
                        text_to_speech(fallback_msg)
                    
                except sr.UnknownValueError:
                    error_msg = "Sorry, I could not understand the audio"
                    print(error_msg)
                    text_to_speech(error_msg)
                    
                except sr.RequestError as e:
                    error_msg = "Could not request results from speech recognition service"
                    print(f"{error_msg}; {e}")
                    text_to_speech(error_msg)
                    
                except KeyboardInterrupt:
                    print("\nGoodbye!")
                    text_to_speech("Goodbye!")
                    break
                    
                except Exception as e:
                    error_msg = "An error occurred. Please try again."
                    print(f"Error: {e}")
                    text_to_speech(error_msg)

if __name__ == "__main__":
    main()
