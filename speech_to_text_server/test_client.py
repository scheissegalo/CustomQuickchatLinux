#!/usr/bin/env python3

import asyncio
import websockets
import json
import sys

async def test_speech_to_text_server(port=8003):
    """Test client for the speech-to-text server"""
    
    uri = f"ws://localhost:{port}"
    
    try:
        print(f"Connecting to speech-to-text server at {uri}...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to server!")
            
            # Test 1: Send a test message
            print("\n🧪 Test 1: Sending test message...")
            test_message = {
                "event": "test",
                "data": {}
            }
            await websocket.send(json.dumps(test_message))
            
            response = await websocket.recv()
            response_data = json.loads(response)
            print(f"📨 Server response: {response_data}")
            
            # Test 2: Test microphone calibration
            print("\n🎤 Test 2: Testing microphone calibration...")
            print("Please stay quiet for a few seconds while the server calibrates...")
            
            calibration_message = {
                "event": "calibrate_microphone",
                "data": {
                    "attemptId": "test_calibration_123"
                }
            }
            await websocket.send(json.dumps(calibration_message))
            
            response = await websocket.recv()
            response_data = json.loads(response)
            print(f"📨 Calibration response: {response_data}")
            
            if response_data.get("event") == "notify_mic_listening":
                print("🎧 Server is listening for calibration...")
                response = await websocket.recv()
                response_data = json.loads(response)
                print(f"📨 Final calibration response: {response_data}")
            
            # Test 3: Test speech-to-text
            print("\n🗣️  Test 3: Testing speech-to-text...")
            print("The server will listen for your voice. Speak something when prompted!")
            
            stt_message = {
                "event": "start_speech_to_text",
                "data": {
                    "args": {
                        "attemptId": "test_stt_456",
                        "beginSpeechTimeout": 5.0,
                        "processSpeechTimeout": 10.0,
                        "autoCalibrateMic": True,
                        "micEnergyThreshold": 420
                    }
                }
            }
            await websocket.send(json.dumps(stt_message))
            
            # Listen for responses
            while True:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=15.0)
                    response_data = json.loads(response)
                    print(f"📨 STT response: {response_data}")
                    
                    if response_data.get("event") == "notify_mic_listening":
                        print("🎧 Server is listening for speech... Speak now!")
                    elif response_data.get("event") == "speech_to_text_result":
                        result = response_data.get("data", {})
                        if result.get("success"):
                            print(f"✅ Success! You said: '{result.get('transcription')}'")
                        else:
                            print(f"❌ Error: {result.get('errorMsg')}")
                        break
                    elif response_data.get("event") == "error_response":
                        print(f"❌ Server error: {response_data.get('data', {}).get('errorMsg')}")
                        break
                        
                except asyncio.TimeoutError:
                    print("⏰ Timeout waiting for response")
                    break
            
            print("\n✅ Test completed!")
            
    except websockets.exceptions.ConnectionRefused:
        print(f"❌ Could not connect to server at {uri}")
        print("Make sure the speech-to-text server is running!")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def main():
    port = 8003
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8003.")
    
    print("🧪 Speech-to-Text Server Test Client")
    print("=" * 40)
    print(f"Testing server on port {port}")
    print("Make sure the speech-to-text server is running first!")
    print("=" * 40)
    
    success = asyncio.run(test_speech_to_text_server(port))
    
    if success:
        print("\n🎉 All tests passed! The speech-to-text server is working correctly.")
    else:
        print("\n💥 Tests failed. Check the server logs for more information.")

if __name__ == "__main__":
    main() 