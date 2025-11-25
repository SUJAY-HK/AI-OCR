import re
import google.generativeai as genai

class MathToSpeech:
    """Converts mathematical notation to speech-friendly text"""
    
    def __init__(self):
        self.greek_letters = {
            'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta',
            'ε': 'epsilon', 'ζ': 'zeta', 'η': 'eta', 'θ': 'theta',
            'ι': 'iota', 'κ': 'kappa', 'λ': 'lambda', 'μ': 'mu',
            'ν': 'nu', 'ξ': 'xi', 'π': 'pi', 'ρ': 'rho',
            'σ': 'sigma', 'τ': 'tau', 'φ': 'phi', 'χ': 'chi',
            'ψ': 'psi', 'ω': 'omega', 'Δ': 'Delta', 'Σ': 'Sigma',
            'Ω': 'Omega', 'Φ': 'Phi', 'Π': 'Pi', 'Θ': 'Theta'
        }
        
        self.operators = {
            '∫': ' integral of ',
            '∑': ' sum of ',
            '∏': ' product of ',
            '∂': ' partial derivative of ',
            '∇': ' gradient of ',
            '√': ' square root of ',
            '∞': ' infinity ',
            '≈': ' approximately equals ',
            '≠': ' not equal to ',
            '≤': ' less than or equal to ',
            '≥': ' greater than or equal to ',
            '±': ' plus or minus ',
            '×': ' times ',
            '÷': ' divided by ',
            '→': ' approaches ',
            '∈': ' is an element of ',
            '⊂': ' is a subset of ',
            '⊆': ' is a subset of or equal to ',
            '∪': ' union ',
            '∩': ' intersection '
        }
    
    def convert_greek_letters(self, text):
        """Convert Greek letters to their names"""
        for symbol, word in self.greek_letters.items():
            text = text.replace(symbol, f' {word} ')
        return text
    
    def convert_operators(self, text):
        """Convert mathematical operators to words"""
        for symbol, word in self.operators.items():
            text = text.replace(symbol, word)
        return text
    
    def convert_superscripts(self, text):
        """Convert superscripts to spoken form"""
        superscripts = {
            '²': ' squared', '³': ' cubed',
            '⁴': ' to the power of 4', '⁵': ' to the power of 5',
            '⁶': ' to the power of 6', '⁷': ' to the power of 7',
            '⁸': ' to the power of 8', '⁹': ' to the power of 9',
            '⁰': ' to the power of 0', '¹': '',
            'ⁿ': ' to the power of n'
        }
        for sup, word in superscripts.items():
            text = text.replace(sup, word)
        
        # Handle x^n pattern
        text = re.sub(r'(\w+)\^(\d+)', r'\1 to the power of \2', text)
        text = re.sub(r'(\w+)\^(\w+)', r'\1 to the power of \2', text)
        text = re.sub(r'(\w+)\^\{(.+?)\}', r'\1 to the power of \2', text)
        return text
    
    def convert_subscripts(self, text):
        """Convert subscripts to spoken form"""
        subscripts = {
            '₀': ' sub 0', '₁': ' sub 1', '₂': ' sub 2',
            '₃': ' sub 3', '₄': ' sub 4', '₅': ' sub 5',
            '₆': ' sub 6', '₇': ' sub 7', '₈': ' sub 8',
            '₉': ' sub 9'
        }
        for sub, word in subscripts.items():
            text = text.replace(sub, word)
        
        # Handle x_n pattern
        text = re.sub(r'(\w+)_(\w+)', r'\1 sub \2', text)
        text = re.sub(r'(\w+)_\{(.+?)\}', r'\1 sub \2', text)
        return text
    
    def convert_fractions(self, text):
        """Convert fractions to spoken form"""
        # Handle simple fractions: a/b
        text = re.sub(r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)', 
                     r'\1 over \2', text)
        return text
    
    def handle_derivatives(self, text):
        """Convert derivative notation to spoken form"""
        # d/dx → "derivative with respect to x"
        text = re.sub(r'd/d(\w+)', r'derivative with respect to \1', text)
        # dy/dx → "derivative of y with respect to x"
        text = re.sub(r'd(\w+)/d(\w+)', 
                     r'derivative of \1 with respect to \2', text)
        # d²y/dx² → "second derivative of y with respect to x"
        text = re.sub(r'd²(\w+)/d(\w+)²', 
                     r'second derivative of \1 with respect to \2', text)
        return text
    
    def remove_markdown(self, text):
        """Remove markdown formatting"""
        text = text.replace('**', '')
        text = text.replace('*', '')
        text = text.replace('`', '')
        text = re.sub(r'#{1,6}\s+', '', text)
        return text
    
    def convert(self, text):
        """Main conversion method"""
        text = self.remove_markdown(text)
        text = self.convert_greek_letters(text)
        text = self.convert_operators(text)
        text = self.handle_derivatives(text)
        text = self.convert_superscripts(text)
        text = self.convert_subscripts(text)
        text = self.convert_fractions(text)
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text)
        return text.strip()


# Supported languages configuration
SUPPORTED_LANGUAGES = {
    'en': {
        'name': 'English',
        'code': 'en',
        'flag': '🇮🇳',
        'tts_lang': 'en'
    },
    'hi': {
        'name': 'Hindi',
        'code': 'hi',
        'flag': '🇮🇳',
        'tts_lang': 'hi'
    },
    'kn': {
        'name': 'Kannada',
        'code': 'kn',
        'flag': '🇮🇳',
        'tts_lang': 'kn'
    },
    'te': {
        'name': 'Telugu',
        'code': 'te',
        'flag': '🇮🇳',
        'tts_lang': 'te'
    },
    'ta': {
        'name': 'Tamil',
        'code': 'ta',
        'flag': '🇮🇳',
        'tts_lang': 'ta'
    },
    'ml': {
        'name': 'Malayalam',
        'code': 'ml',
        'flag': '🇮🇳',
        'tts_lang': 'ml'
    }
}


def translate_with_gemini(text, target_language, gemini_api_key):
    """
    Translate English text to target Indian language using Gemini
    Keeps mathematical terms in English for clarity
    """
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
    
    language_name = SUPPORTED_LANGUAGES.get(target_language, {}).get('name', target_language)
    
    prompt = f"""Translate the following mathematical explanation from English to {language_name}.

IMPORTANT RULES:
1. Keep all mathematical terms, numbers, and variable names in ENGLISH (do not translate)
2. Keep technical terms like "derivative", "integral", "equation" in English
3. Only translate the connecting words and explanatory phrases
4. Maintain the same structure and clarity
5. Make it sound natural when read aloud in {language_name}
6. Keep it simple and easy to understand

Examples of what to keep in English:
- Numbers: 1, 2, 3, x, y, z
- Math terms: derivative, integral, equation, sum, limit
- Variables: alpha, beta, theta, x squared, etc.

Text to translate:
{text}

Provide only the translated version:"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Translation error: {e}")
        # Fallback: return original text if translation fails
        return text


def refine_with_gemini(text, gemini_api_key, target_language='en'):
    """
    Use Gemini to refine the speech text for natural delivery
    """
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
    
    if target_language == 'en':
        prompt = f"""Convert this mathematical explanation to a format perfect for text-to-speech audio narration.

Requirements:
1. Make it sound natural and conversational when read aloud
2. Ensure all mathematical terms are clearly expressed
3. Add appropriate transitions and pauses (use commas and periods)
4. Keep the educational value and accuracy
5. Make it easy to follow when listening
6. Use phrases like "which means", "this gives us", "we can see that" for better flow
7. Don't use markdown or special formatting

Text to convert:
{text}

Provide only the refined speech-ready version:"""
    else:
        language_name = SUPPORTED_LANGUAGES.get(target_language, {}).get('name', target_language)
        prompt = f"""Refine this {language_name} mathematical explanation for text-to-speech audio narration.

Requirements:
1. Make it sound natural when read aloud in {language_name}
2. Add appropriate pauses with commas and periods
3. Keep mathematical terms in English
4. Keep it clear and educational
5. Don't use markdown or special formatting

Text to refine:
{text}

Provide only the refined version:"""

    response = model.generate_content(prompt)
    return response.text


def generate_audio_summary(text, output_path, gemini_api_key, language='en'):
    """
    Generate audio from text using gTTS in specified language
    
    Args:
        text: The explanation text to convert to audio
        output_path: Path where the audio file will be saved
        gemini_api_key: Gemini API key for refinement and translation
        language: Language code (en, hi, kn, te, ta, ml)
    
    Returns:
        str: Path to the generated audio file
    """
    try:
        from gtts import gTTS
    except ImportError:
        raise ImportError(
            "gTTS not installed. Install it with: pip install gTTS"
        )
    
    # Validate language
    if language not in SUPPORTED_LANGUAGES:
        print(f"Warning: Unsupported language '{language}', falling back to English")
        language = 'en'
    
    # Step 1: Convert math notation to speech-friendly text
    converter = MathToSpeech()
    speech_text = converter.convert(text)
    
    # Step 2: Translate if not English
    if language != 'en':
        try:
            print(f"Translating to {SUPPORTED_LANGUAGES[language]['name']}...")
            speech_text = translate_with_gemini(speech_text, language, gemini_api_key)
        except Exception as e:
            print(f"Warning: Translation failed ({e}), using English")
            language = 'en'
    
    # Step 3: Refine with Gemini for natural delivery
    try:
        refined_text = refine_with_gemini(speech_text, gemini_api_key, language)
    except Exception as e:
        print(f"Warning: Gemini refinement failed ({e}), using basic conversion")
        refined_text = speech_text
    
    # Step 4: Generate audio using gTTS
    try:
        # Get the correct gTTS language code
        tts_lang = SUPPORTED_LANGUAGES[language]['tts_lang']
        
        # Create gTTS object
        tts = gTTS(text=refined_text, lang=tts_lang, slow=False)
        
        # Save the audio file
        tts.save(output_path)
        
        print(f"✅ Audio generated successfully in {SUPPORTED_LANGUAGES[language]['name']}: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error generating audio with gTTS: {e}")
        raise


def generate_audio_with_ssml(text, output_path, gemini_api_key, language='en'):
    """
    Alias for generate_audio_summary for compatibility
    """
    return generate_audio_summary(text, output_path, gemini_api_key, language)


def get_supported_languages():
    """
    Return list of supported languages for the frontend
    """
    return SUPPORTED_LANGUAGES