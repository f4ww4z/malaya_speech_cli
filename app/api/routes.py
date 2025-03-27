from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import FileResponse
import os
import uuid
import tempfile
from malaya_speech import tts
from malaya_speech.utils.astype import float_to_int
import scipy.io.wavfile as wavfile
from typing import Dict, List
import time
import zipfile
import io

from .models import TTSRequest, TTSResponse, TTSBatchRequest, TTSBatchResponse, VoiceModel

router = APIRouter()

AUDIO_DIR = "app/static/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

SAMPLE_RATE = 22050  # Sample rate for TTS models

# Cache for loaded models to improve performance
model_cache: Dict[str, any] = {}

@router.get("/models", response_model=List[VoiceModel])
async def get_models():
    """Get all available TTS models"""
    models = []
    available_models = tts.available_vits()
    
    for model_name, info in available_models.items():
        # Create a user-friendly display name from the model name
        display_name = model_name.split('/')[-1].replace('VITS-', '')
        display_name = display_name.capitalize()
        
        models.append(
            VoiceModel(
                name=model_name,
                display_name=display_name,
                size_mb=info.get('Size (MB)', 0),
                understands_punctuation=info.get('Understand punctuation', False),
                is_lowercase=info.get('Is lowercase', False)
            )
        )
    
    return models

def get_tts_model(model_name: str):
    """Get or load a TTS model"""
    if model_name not in model_cache:
        try:
            model_cache[model_name] = tts.vits(model=model_name)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to load model: {str(e)}")
    return model_cache[model_name]

@router.post("/synthesize", response_model=TTSResponse)
async def synthesize_speech(request: TTSRequest):
    """Synthesize speech from text"""
    try:
        model = get_tts_model(request.model)
        
        # Generate audio
        result = model.predict(
            request.text, 
            temperature=request.temperature, 
            length_ratio=request.length_ratio
        )
        
        # Convert float audio to int16
        audio_int = float_to_int(result['y'])
        
        # Create unique filename
        filename = f"{int(time.time())}_{uuid.uuid4().hex[:8]}.wav"
        filepath = os.path.join(AUDIO_DIR, filename)
        
        # Save with proper sample rate using scipy
        wavfile.write(filepath, SAMPLE_RATE, audio_int)
        
        return TTSResponse(
            filename=filename,
            audio_url=f"/static/audio/{filename}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating speech: {str(e)}")

@router.post("/synthesize-batch", response_model=TTSBatchResponse)
async def synthesize_batch(request: TTSBatchRequest):
    """Synthesize speech for multiple lines of text"""
    try:
        model = get_tts_model(request.model)
        responses = []
        
        for line in request.lines:
            if not line.strip():
                continue
                
            # Generate audio
            result = model.predict(
                line, 
                temperature=request.temperature, 
                length_ratio=request.length_ratio
            )
            
            # Convert float audio to int16
            audio_int = float_to_int(result['y'])
            
            # Create unique filename
            filename = f"{int(time.time())}_{uuid.uuid4().hex[:8]}.wav"
            filepath = os.path.join(AUDIO_DIR, filename)
            
            # Save with proper sample rate using scipy
            wavfile.write(filepath, SAMPLE_RATE, audio_int)
            
            responses.append(
                TTSResponse(
                    filename=filename,
                    audio_url=f"/static/audio/{filename}"
                )
            )
        
        return TTSBatchResponse(files=responses)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating batch speech: {str(e)}")

@router.get("/download/{filename}")
async def download_audio(filename: str):
    """Download an audio file"""
    filepath = os.path.join(AUDIO_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        filepath, 
        media_type="audio/wav", 
        filename=filename
    )

@router.post("/download-zip", response_class=Response)
async def download_zip(filenames: List[str]):
    """Download multiple audio files as a ZIP archive"""
    if not filenames:
        raise HTTPException(status_code=400, detail="No files specified for download")
    
    try:
        # Create a BytesIO object to store the ZIP file
        zip_io = io.BytesIO()
        
        # Create a ZIP file
        with zipfile.ZipFile(zip_io, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for filename in filenames:
                filepath = os.path.join(AUDIO_DIR, filename)
                
                if not os.path.exists(filepath):
                    continue  # Skip files that don't exist
                
                # Add file to ZIP
                zip_file.write(filepath, filename)
        
        # Reset file pointer to start
        zip_io.seek(0)
        
        # Create response with ZIP file
        return Response(
            content=zip_io.getvalue(),
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename=malaya_speech_audio_{int(time.time())}.zip"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating ZIP file: {str(e)}")