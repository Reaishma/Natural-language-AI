"""
Language Translation Module
Translates text between languages using deep-translator
"""
import streamlit as st
from deep_translator import GoogleTranslator
from typing import Dict, Any, List
import pandas as pd

class LanguageTranslator:
    def __init__(self):
        self.languages = GoogleTranslator().get_supported_languages(as_dict=True)
        
        self.popular_languages = {
            'english': 'en',
            'spanish': 'es',
            'french': 'fr',
            'german': 'de',
            'italian': 'it',
            'portuguese': 'pt',
            'russian': 'ru',
            'japanese': 'ja',
            'korean': 'ko',
            'chinese (simplified)': 'zh-CN',
            'arabic': 'ar',
            'hindi': 'hi',
            'dutch': 'nl',
            'swedish': 'sv',
            'danish': 'da',
            'norwegian': 'no',
            'finnish': 'fi',
            'polish': 'pl',
            'turkish': 'tr',
            'thai': 'th'
        }
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of input text
        """
        try:
            if not text or len(text.strip()) < 3:
                return {"error": "Text too short for language detection"}
            
            from deep_translator import single_detection
            detected_lang = single_detection(text, api_key=None)
            
            return {
                "language_code": detected_lang,
                "language_name": detected_lang.title(),
                "confidence": 0.95,
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
            
            translator = GoogleTranslator(source='auto' if source_lang == 'auto' else source_lang, target=target_lang)
            translated_text = translator.translate(text)
            
            return {
                "translated_text": translated_text,
                "source_language": source_lang,
                "source_language_name": source_lang.title() if source_lang != 'auto' else 'Auto-detected',
                "target_language": target_lang,
                "target_language_name": target_lang.title(),
                "original_text": text,
                "original_length": len(text),
                "translated_length": len(translated_text)
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
                            "text": text[:50] + "...",
                            "error": translation_result["error"]
                        })
            
            return {
                "translations": results,
                "total_texts": len(texts),
                "successful": len(results),
                "failed": len(failed_translations),
                "failed_translations": failed_translations,
                "target_language": target_lang
            }
            
        except Exception as e:
            return {"error": f"Batch translation failed: {str(e)}"}
    
    def translate_with_alternatives(self, text: str, target_languages: List[str], source_lang: str = 'auto') -> Dict[str, Any]:
        """
        Translate text to multiple target languages
        """
        try:
            translations = {}
            
            for target_lang in target_languages:
                result = self.translate_text(text, target_lang, source_lang)
                if "error" not in result:
                    translations[target_lang] = {
                        "translated_text": result["translated_text"],
                        "language_name": result["target_language_name"]
                    }
                else:
                    translations[target_lang] = {
                        "error": result["error"],
                        "language_name": target_lang.title()
                    }
            
            return {
                "original_text": text,
                "source_language": source_lang,
                "translations": translations,
                "total_languages": len(target_languages)
            }
            
        except Exception as e:
            return {"error": f"Multi-language translation failed: {str(e)}"}


def create_translation_interface():
    """
    Create the Streamlit interface for language translation
    """
    st.header("🌍 Language Translation")
    st.write("Translate text between multiple languages with automatic language detection.")
    
    translator = LanguageTranslator()
    
    translation_mode = st.selectbox(
        "Choose translation mode:",
        ["Single Text Translation", "Batch Translation", "Multi-Language Translation", "Language Detection"]
    )
    
    if translation_mode == "Single Text Translation":
        st.subheader("📝 Single Text Translation")
        
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
        
        col1, col2 = st.columns(2)
        
        with col1:
            source_lang = st.selectbox(
                "Source Language:",
                ["auto"] + list(translator.popular_languages.values()),
                format_func=lambda x: "Auto-detect" if x == "auto" else [k for k, v in translator.popular_languages.items() if v == x][0].title() if x in translator.popular_languages.values() else x
            )
        
        with col2:
            target_lang = st.selectbox(
                "Target Language:",
                list(translator.popular_languages.values()),
                format_func=lambda x: [k for k, v in translator.popular_languages.items() if v == x][0].title() if x in translator.popular_languages.values() else x,
                index=1
            )
        
        if st.button("Translate", type="primary"):
            if text_to_translate and len(text_to_translate.strip()) > 0:
                with st.spinner("Translating..."):
                    result = translator.translate_text(text_to_translate, target_lang, source_lang)
                    
                    if "error" not in result:
                        st.subheader("✅ Translation Result")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Source Language", result["source_language_name"])
                        with col2:
                            st.metric("Target Language", result["target_language_name"])
                        
                        st.text_area("Translated Text:", value=result["translated_text"], height=150)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Original Length", f"{result['original_length']} chars")
                        with col2:
                            st.metric("Translated Length", f"{result['translated_length']} chars")
                        
                        from utils.helpers import create_download_link
                        create_download_link(
                            result["translated_text"],
                            "translation.txt",
                            "📥 Download Translation"
                        )
                    
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
            else:
                from utils.helpers import display_error
                display_error("Please enter text to translate.")
    
    elif translation_mode == "Batch Translation":
        st.subheader("📚 Batch Translation")
        st.info("Translate multiple texts at once.")
        
        texts_input = st.text_area(
            "Enter texts (one per line):",
            height=200,
            placeholder="Enter each text on a new line..."
        )
        
        target_lang = st.selectbox(
            "Target Language:",
            list(translator.popular_languages.values()),
            format_func=lambda x: [k for k, v in translator.popular_languages.items() if v == x][0].title() if x in translator.popular_languages.values() else x
        )
        
        if st.button("Translate All", type="primary"):
            if texts_input:
                texts = [t.strip() for t in texts_input.split('\n') if t.strip()]
                
                if texts:
                    with st.spinner(f"Translating {len(texts)} texts..."):
                        result = translator.batch_translate(texts, target_lang)
                        
                        if "error" not in result:
                            st.subheader("📊 Translation Results")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Texts", result["total_texts"])
                            with col2:
                                st.metric("Successful", result["successful"])
                            with col3:
                                st.metric("Failed", result["failed"])
                            
                            if result["translations"]:
                                st.subheader("✅ Translations")
                                for trans in result["translations"]:
                                    with st.expander(f"Text {trans['index']}: {trans['original'][:50]}..."):
                                        st.write(f"**Original:** {trans['full_original']}")
                                        st.write(f"**Translated:** {trans['full_translated']}")
                            
                            if result["failed_translations"]:
                                st.subheader("❌ Failed Translations")
                                for failed in result["failed_translations"]:
                                    st.error(f"Text {failed['index']}: {failed['error']}")
                        
                        else:
                            from utils.helpers import display_error
                            display_error(result["error"])
                else:
                    from utils.helpers import display_error
                    display_error("Please enter at least one text.")
            else:
                from utils.helpers import display_error
                display_error("Please enter texts to translate.")
    
    elif translation_mode == "Multi-Language Translation":
        st.subheader("🌐 Multi-Language Translation")
        st.info("Translate one text into multiple languages simultaneously.")
        
        text_to_translate = st.text_area(
            "Enter text to translate:",
            height=120,
            placeholder="Enter the text you want to translate..."
        )
        
        target_languages = st.multiselect(
            "Select target languages:",
            list(translator.popular_languages.values()),
            format_func=lambda x: [k for k, v in translator.popular_languages.items() if v == x][0].title() if x in translator.popular_languages.values() else x,
            default=[translator.popular_languages['spanish'], translator.popular_languages['french']]
        )
        
        if st.button("Translate to All", type="primary"):
            if text_to_translate and target_languages:
                with st.spinner(f"Translating to {len(target_languages)} languages..."):
                    result = translator.translate_with_alternatives(text_to_translate, target_languages)
                    
                    if "error" not in result:
                        st.subheader("🌍 Translations")
                        
                        for lang_code, translation_data in result["translations"].items():
                            if "error" not in translation_data:
                                st.success(f"**{translation_data['language_name']}:**")
                                st.write(translation_data["translated_text"])
                                st.write("---")
                            else:
                                st.error(f"**{translation_data['language_name']}:** {translation_data['error']}")
                        
                        download_content = f"Original Text:\n{result['original_text']}\n\n"
                        download_content += "=" * 50 + "\n"
                        download_content += "TRANSLATIONS\n"
                        download_content += "=" * 50 + "\n\n"
                        
                        for lang_code, translation_data in result["translations"].items():
                            if "error" not in translation_data:
                                download_content += f"{translation_data['language_name']}:\n"
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
                        
                        st.subheader("📝 Analyzed Text")
                        st.info(text_to_detect[:300] + "..." if len(text_to_detect) > 300 else text_to_detect)
                        
                        st.caption(f"Text length: {result['text_length']} characters")
                    
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
            else:
                from utils.helpers import display_error
                display_error("Please enter text for language detection.")
