// Animation configurations
const soundWaveAnimation = {
    container: document.getElementById('animation-container'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: 'https://assets8.lottiefiles.com/packages/lf20_7qispsae.json'
};

const loadingAnimation = {
    container: document.getElementById('loading-animation'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: 'https://assets5.lottiefiles.com/packages/lf20_usmfx6bp.json'
};

// Initialize animations
const headerAnimation = lottie.loadAnimation(soundWaveAnimation);
const loading = lottie.loadAnimation(loadingAnimation);

// DOM elements
const voiceModelSelect = document.getElementById('voice-model');
const textInput = document.getElementById('text-input');
const convertBtn = document.getElementById('convert-btn');
const clearBtn = document.getElementById('clear-btn');
const resultsContainer = document.getElementById('results-container');
const audioResults = document.getElementById('audio-results');
const loadingOverlay = document.getElementById('loading-overlay');
const downloadAllBtn = document.getElementById('download-all-btn');

// API base URL
const API_BASE_URL = '/api';

// Store all generated audio files
let generatedAudioFiles = [];

// Fetch available voice models
async function fetchVoiceModels() {
    try {
        const response = await fetch(`${API_BASE_URL}/models`);
        if (!response.ok) {
            throw new Error('Failed to fetch models');
        }
        
        const models = await response.json();
        
        // Clear loading option
        voiceModelSelect.innerHTML = '';
        
        // Add models to select element
        models.forEach(model => {
            const option = document.createElement('option');
            option.value = model.name;
            option.textContent = model.display_name;
            voiceModelSelect.appendChild(option);
        });
        
        // Enable first option if available
        if (models.length > 0) {
            voiceModelSelect.value = models[0].name;
        }
    } catch (error) {
        console.error('Error fetching models:', error);
        showError('Failed to load voice models. Please refresh the page.');
    }
}

// Convert text to speech
async function convertTextToSpeech() {
    const text = textInput.value.trim();
    const model = voiceModelSelect.value;
    
    if (!text) {
        showError('Please enter some text to convert');
        return;
    }
    
    if (!model) {
        showError('Please select a voice model');
        return;
    }
    
    // Show loading overlay
    loadingOverlay.style.display = 'flex';
    
    try {
        // Split text into lines and filter out empty lines
        const lines = text.split('\n').filter(line => line.trim());
        
        if (lines.length === 0) {
            throw new Error('No valid text to convert');
        }
        
        // Create batch request
        const batchRequest = {
            lines: lines,
            model: model,
            temperature: 0.6666,
            length_ratio: 1.0
        };
        
        // Send request to API
        const response = await fetch(`${API_BASE_URL}/synthesize-batch`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(batchRequest)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate speech');
        }
        
        const result = await response.json();
        
        // Clear previous results
        audioResults.innerHTML = '';
        generatedAudioFiles = [];
        
        // Process each generated audio file
        result.files.forEach((file, index) => {
            const text = lines[index];
            generatedAudioFiles.push({
                text: text,
                url: file.audio_url,
                filename: file.filename
            });
            
            // Create audio item
            createAudioItem(text, file.audio_url, file.filename, index);
        });
        
        // Show results container and download all button
        resultsContainer.style.display = 'block';
        downloadAllBtn.style.display = 'block';
        
        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Error generating speech:', error);
        showError(error.message || 'Failed to generate speech. Please try again.');
    } finally {
        // Hide loading overlay
        loadingOverlay.style.display = 'none';
    }
}

// Create audio item in the results section
function createAudioItem(text, audioUrl, filename, index) {
    const audioItem = document.createElement('div');
    audioItem.className = 'audio-item';
    audioItem.innerHTML = `
        <div class="audio-text" title="${text}">
            <strong>Line ${index + 1}:</strong> ${text}
        </div>
        <div class="audio-controls">
            <audio controls src="${audioUrl}"></audio>
            <button class="download-btn" data-url="${audioUrl}" data-filename="${filename}">
                <i class="fas fa-download"></i>
            </button>
        </div>
    `;
    
    // Add download event listener
    const downloadBtn = audioItem.querySelector('.download-btn');
    downloadBtn.addEventListener('click', () => {
        downloadAudio(audioUrl, text);
    });
    
    audioResults.appendChild(audioItem);
}

// Download a single audio file
function downloadAudio(url, text) {
    // Create filename from text (first 15 chars)
    const sanitizedText = text.substring(0, 15).replace(/[^a-z0-9]/gi, '_');
    const filename = `${sanitizedText}.wav`;
    
    // Create a temporary link
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Download all generated audio files as a ZIP
async function downloadAllAudioFiles() {
    if (generatedAudioFiles.length === 0) {
        showError('No audio files to download');
        return;
    }
    
    try {
        // Show loading overlay with different message
        loadingOverlay.querySelector('p').textContent = 'Creating ZIP file...';
        loadingOverlay.style.display = 'flex';
        
        // Get all filenames
        const filenames = generatedAudioFiles.map(file => file.filename);
        
        // Call the API to create a ZIP file
        const response = await fetch(`${API_BASE_URL}/download-zip`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(filenames)
        });
        
        if (!response.ok) {
            throw new Error('Failed to create ZIP file');
        }
        
        // Get the blob from the response
        const blob = await response.blob();
        
        // Create a URL for the blob
        const url = window.URL.createObjectURL(blob);
        
        // Create a link to download the ZIP
        const link = document.createElement('a');
        link.href = url;
        link.download = `malaya_speech_audio_${Date.now()}.zip`;
        document.body.appendChild(link);
        
        // Click the link to download the file
        link.click();
        
        // Clean up
        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);
    } catch (error) {
        console.error('Error downloading ZIP:', error);
        showError('Failed to download ZIP file. Please try again.');
    } finally {
        // Hide loading overlay and reset message
        loadingOverlay.style.display = 'none';
        loadingOverlay.querySelector('p').textContent = 'Generating speech...';
    }
}

// Show an error message
function showError(message) {
    // You can implement a nicer error display here
    alert(message);
}

// Clear the form
function clearForm() {
    textInput.value = '';
    // Don't hide results for better UX
}

// Initialize the app
function initApp() {
    // Load voice models
    fetchVoiceModels();
    
    // Event listeners
    convertBtn.addEventListener('click', convertTextToSpeech);
    clearBtn.addEventListener('click', clearForm);
    downloadAllBtn.addEventListener('click', downloadAllAudioFiles);
}

// Start the app
document.addEventListener('DOMContentLoaded', initApp);