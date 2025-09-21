"""
Language Translation Module
Translates text between multiple languages using googletrans
"""
import streamlit as st
from googletrans import Translator, LANGUAGES
import pandas as pd
from typing import Dict, Any, List
import time

class LanguageTranslator:
    def __init__(self):
        self.translator = Translator()
        self.languages = LANGUAGES
        
        # Popular language mappings for better UX
        self.popular_languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'da': 'Danish',
            'no': 'Norwegian',
            'fi': 'Finnish',
            'pl': 'Polish',
            'tr': 'Turkish',
            'th': 'Thai'
        }
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of input text
        """
        try:
            if not text or len(text.strip()) < 3:
                return {"error": "Text too short for language detection"}
            
            detection = self.translator.detect(text)
            
            detected_lang = detection.lang
            confidence = detection.confidence
            language_name = self.languages.get(detected_lang, "Unknown")
            
            return {
                "language_code": detected_lang,
                "language_name": language_name,
                "confidence": confidence,
                "text_length": len(text)
            }
            
        except Exception as e:
            return {"error": f"Language detection failed: {str(e)}"}
    
    def translate_text(self, text: str, target_lang: str, source_lang: str = 'auto') -> Dict[str, Any]:
        """
        Translate text from source language to target language
        """
        try:
            if not text or len(text.strip()) < 1:
                return {"error": "Text is empty"}
            
            # Detect source language if auto
            if source_lang == 'auto':
                detection = self.detect_language(text)
                if "error" in detection:
                    return detection
                detected_lang = detection["language_code"]
            else:
                detected_lang = source_lang
            
            # Perform translation
            translation = self.translator.translate(
                text, 
                src=detected_lang if source_lang == 'auto' else source_lang,
                dest=target_lang
            )
            
            return {
                "translated_text": translation.text,
                "source_language": detected_lang,
                "source_language_name": self.languages.get(detected_lang, "Unknown"),
                "target_language": target_lang,
                "target_language_name": self.languages.get(target_lang, "Unknown"),
                "original_text": text,
                "original_length": len(text),
                "translated_length": len(translation.text)
            }
            
        except Exception as e:
            return {"error": f"Translation failed: {str(e)}"}
    
    def batch_translate(self, texts: List[str], target_lang: str, source_lang: str = 'auto') -> Dict[str, Any]:
        """
        Translate multiple texts in batch
        """
        try:
            results = []
            failed_translations = []
            
            for i, text in enumerate(texts):
                if text and len(text.strip()) > 0:
                    translation_result = self.translate_text(text, target_lang, source_lang)
                    
                    if "error" not in translation_result:
                        results.append({
                            "index": i + 1,
                            "original": text[:100] + "..." if len(text) > 100 else text,
                            "translated": translation_result["translated_text"][:100] + "..." if len(translation_result["translated_text"]) > 100 else translation_result["translated_text"],
                            "source_lang": translation_result["source_language_name"],
                            "full_original": text,
                            "full_translated": translation_result["translated_text"]
                        })
                    else:
                        failed_translations.append({
                            "index": i + 1,
                            "text": text[:50] + "..." if len(text) > 50 else text,
                            "error": translation_result["error"]
                        })
            
            return {
                "successful_translations": results,
                "failed_translations": failed_translations,
                "success_count": len(results),
                "failure_count": len(failed_translations),
                "total_count": len(texts)
            }
            
        except Exception as e:
            return {"error": f"Batch translation failed: {str(e)}"}
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get list of supported languages
        """
        return self.languages
    
    def translate_with_alternatives(self, text: str, target_langs: List[str], source_lang: str = 'auto') -> Dict[str, Any]:
        """
        Translate text to multiple target languages
        """
        try:
            translations = {}
            
            for lang_code in target_langs:
                result = self.translate_text(text, lang_code, source_lang)
                if "error" not in result:
                    translations[lang_code] = {
                        "language_name": result["target_language_name"],
                        "translated_text": result["translated_text"]
                    }
                else:
                    translations[lang_code] = {
                        "language_name": self.languages.get(lang_code, "Unknown"),
                        "error": result["error"]
                    }
            
            return {
                "original_text": text,
                "translations": translations,
                "target_languages": len(target_langs),
                "successful_translations": len([t for t in translations.values() if "error" not in t])
            }
            
        except Exception as e:
            return {"error": f"Multi-language translation failed: {str(e)}"}

# Streamlit interface for language translation
def create_translation_interface():
    """
    Create the Streamlit interface for language translation
    """
    st.header("🌍 Language Translation")
    st.write("Translate text between multiple languages with automatic language detection.")
    
    translator = LanguageTranslator()
    
    # Translation mode selection
    translation_mode = st.selectbox(
        "Choose translation mode:",
        ["Single Text Translation", "Batch Translation", "Multi-Language Translation", "Language Detection"]
    )
    
    if translation_mode == "Single Text Translation":
        st.subheader("📝 Single Text Translation")
        
        # Input options
        input_method = st.radio("Choose input method:", ["Text Input", "File Upload"])
        
        text_to_translate = ""
        
        if input_method == "Text Input":
            text_to_translate = st.text_area(
                "Enter text to translate:",
                height=150,
                placeholder="Type or paste your text here..."
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload a text file:",
                type=['txt'],
                help="Upload a .txt file to translate"
            )
            if uploaded_file:
                from utils.helpers import handle_file_upload
                text_to_translate = handle_file_upload(uploaded_file)
        
        # Language selection
        col1, col2 = st.columns(2)
        
        with col1:
            source_lang = st.selectbox(
                "Source Language:",
                ["auto"] + list(translator.popular_languages.keys()),
                format_func=lambda x: "Auto-detect" if x == "auto" else translator.popular_languages.get(x, x)
            )
        
        with col2:
            target_lang = st.selectbox(
                "Target Language:",
                list(translator.popular_languages.keys()),
                format_func=lambda x: translator.popular_languages.get(x, x),
                index=1  # Default to Spanish
            )
        
        if st.button("Translate", type="primary"):
            if text_to_translate and len(text_to_translate.strip()) > 0:
                with st.spinner("Translating..."):
                    result = translator.translate_text(text_to_translate, target_lang, source_lang)
                    
                    if "error" not in result:
                        # Display translation
                        st.subheader("✅ Translation Result")
                        
                        # Language info
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"**From:** {result['source_language_name']} ({result['source_language']})")
                        with col2:
                            st.info(f"**To:** {result['target_language_name']} ({result['target_language']})")
                        
                        # Original and translated text
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("Original Text")
                            st.write(result["original_text"])
                        
                        with col2:
                            st.subheader("Translated Text")
                            st.success(result["translated_text"])
                        
                        # Statistics
                        st.subheader("📊 Translation Statistics")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Original Length", f"{result['original_length']} chars")
                        with col2:
                            st.metric("Translated Length", f"{result['translated_length']} chars")
                        with col3:
                            ratio = result['translated_length'] / result['original_length'] if result['original_length'] > 0 else 0
                            st.metric("Length Ratio", f"{ratio:.2f}")
                        
                        # Download option
                        from utils.helpers import create_download_link
                        download_content = f"Original ({result['source_language_name']}):\n{result['original_text']}\n\nTranslated ({result['target_language_name']}):\n{result['translated_text']}"
                        create_download_link(
                            download_content,
                            f"translation_{result['source_language']}_to_{result['target_language']}.txt",
                            "📥 Download Translation"
                        )
                    
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
            else:
                from utils.helpers import display_error
                display_error("Please enter some text to translate.")
    
    elif translation_mode == "Batch Translation":
        st.subheader("📚 Batch Translation")
        st.info("Translate multiple texts at once.")
        
        # Input texts
        num_texts = st.slider("Number of texts:", min_value=2, max_value=10, value=3)
        
        texts = []
        for i in range(num_texts):
            text = st.text_area(f"Text {i+1}:", height=80, key=f"batch_text_{i}")
            if text:
                texts.append(text)
        
        # Language selection
        col1, col2 = st.columns(2)
        with col1:
            source_lang = st.selectbox(
                "Source Language:",
                ["auto"] + list(translator.popular_languages.keys()),
                format_func=lambda x: "Auto-detect" if x == "auto" else translator.popular_languages.get(x, x),
                key="batch_source"
            )
        
        with col2:
            target_lang = st.selectbox(
                "Target Language:",
                list(translator.popular_languages.keys()),
                format_func=lambda x: translator.popular_languages.get(x, x),
                index=1,
                key="batch_target"
            )
        
        if st.button("Translate All", type="primary"):
            if len(texts) >= 1:
                with st.spinner(f"Translating {len(texts)} texts..."):
                    result = translator.batch_translate(texts, target_lang, source_lang)
                    
                    if "error" not in result:
                        # Success summary
                        st.subheader("📊 Translation Summary")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Successful", result["success_count"])
                        with col2:
                            st.metric("Failed", result["failure_count"])
                        with col3:
                            st.metric("Total", result["total_count"])
                        
                        # Successful translations
                        if result["successful_translations"]:
                            st.subheader("✅ Successful Translations")
                            for translation in result["successful_translations"]:
                                with st.expander(f"Translation {translation['index']} ({translation['source_lang']})"):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write("**Original:**")
                                        st.write(translation["full_original"])
                                    with col2:
                                        st.write("**Translated:**")
                                        st.success(translation["full_translated"])
                        
                        # Failed translations
                        if result["failed_translations"]:
                            st.subheader("❌ Failed Translations")
                            for failure in result["failed_translations"]:
                                st.error(f"**Text {failure['index']}:** {failure['error']}")
                                st.caption(f"Text: {failure['text']}")
                        
                        # Download batch results
                        if result["successful_translations"]:
                            batch_content = ""
                            for i, translation in enumerate(result["successful_translations"], 1):
                                batch_content += f"=== Translation {i} ===\n"
                                batch_content += f"Original: {translation['full_original']}\n"
                                batch_content += f"Translated: {translation['full_translated']}\n\n"
                            
                            from utils.helpers import create_download_link
                            create_download_link(
                                batch_content,
                                "batch_translations.txt",
                                "📥 Download All Translations"
                            )
                    
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
            else:
                from utils.helpers import display_error
                display_error("Please enter at least one text to translate.")
    
    elif translation_mode == "Multi-Language Translation":
        st.subheader("🌐 Multi-Language Translation")
        st.info("Translate one text into multiple languages.")
        
        text_to_translate = st.text_area(
            "Enter text to translate:",
            height=120,
            placeholder="Enter the text you want to translate to multiple languages..."
        )
        
        st.write("Select target languages:")
        target_languages = st.multiselect(
            "Target Languages:",
            list(translator.popular_languages.keys()),
            format_func=lambda x: translator.popular_languages.get(x, x),
            default=['es', 'fr', 'de']
        )
        
        if st.button("Translate to All Languages", type="primary"):
            if text_to_translate and target_languages:
                with st.spinner(f"Translating to {len(target_languages)} languages..."):
                    result = translator.translate_with_alternatives(text_to_translate, target_languages)
                    
                    if "error" not in result:
                        st.subheader("🎯 Multi-Language Results")
                        
                        # Summary
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Target Languages", result["target_languages"])
                        with col2:
                            st.metric("Successful", result["successful_translations"])
                        
                        # Display original text
                        st.subheader("📝 Original Text")
                        st.info(result["original_text"])
                        
                        # Display translations
                        st.subheader("🌍 Translations")
                        
                        for lang_code, translation_data in result["translations"].items():
                            if "error" not in translation_data:
                                st.success(f"**{translation_data['language_name']} ({lang_code}):**")
                                st.write(translation_data["translated_text"])
                                st.write("---")
                            else:
                                st.error(f"**{translation_data['language_name']} ({lang_code}):** {translation_data['error']}")
                        
                        # Download all translations
                        download_content = f"Original Text:\n{result['original_text']}\n\n"
                        download_content += "=" * 50 + "\n"
                        download_content += "TRANSLATIONS\n"
                        download_content += "=" * 50 + "\n\n"
                        
                        for lang_code, translation_data in result["translations"].items():
                            if "error" not in translation_data:
                                download_content += f"{translation_data['language_name']} ({lang_code}):\n"
                                download_content += f"{translation_data['translated_text']}\n\n"
                        
                        from utils.helpers import create_download_link
                        create_download_link(
                            download_content,
                            "multi_language_translations.txt",
                            "📥 Download All Translations"
                        )
                    
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
            else:
                from utils.helpers import display_error
         display_error("Please enter text and select at least one target language.")
    
    elif translation_mode == "Language Detection":
        st.subheader("🔍 Language Detection")
        st.info("Detect the language of any text automatically.")
        
        text_to_detect = st.text_area(
            "Enter text for language detection:",
            height=120,
            placeholder="Enter any text and I'll detect its language..."
        )
        
        if st.button("Detect Language", type="primary"):
            if text_to_detect and len(text_to_detect.strip()) > 0:
                with st.spinner("Detecting language..."):
                    result = translator.detect_language(text_to_detect)
                    
                    if "error" not in result:
                        st.subheader("🎯 Detection Result")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Language", result["language_name"])
                        with col2:
                            st.metric("Language Code", result["language_code"])
                        with col3:
                            st.metric("Confidence", f"{result['confidence']:.1%}")
                        
                        # Show text preview
                        st.subheader("📝 Analyzed Text")
                        st.info(text_to_detect[:300] + "..." if len(text_to_detect) > 300 else text_to_detect)
                        
                        st.caption(f"Text length: {result['text_length']} characters")
                    
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
            else:
                from utils.helpers import display_error
                display_error("Please enter some text for language detection.")

if __name__ == "__main__":
    create_translation_interface()
