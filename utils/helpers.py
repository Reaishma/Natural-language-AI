"""
Utility functions for the NLP Virtual Assistant
"""
import streamlit as st
import pandas as pd
from typing import List, Dict, Any
import io

def display_results(results: Dict[str, Any], result_type: str):
    """
    Display results in a user-friendly format based on the result type
    """
    if result_type == "sentiment":
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Sentiment", results.get("sentiment", "Unknown"))
        with col2:
            st.metric("Confidence", f"{results.get('confidence', 0):.2f}")
        
        if "scores" in results:
            st.subheader("Detailed Scores")
            df = pd.DataFrame([results["scores"]])
            st.dataframe(df)
    
    elif result_type == "entities":
        if results.get("entities"):
            st.subheader("Named Entities Found")
            df = pd.DataFrame(results["entities"])
            st.dataframe(df)
        else:
            st.info("No named entities found in the text.")
    
    elif result_type == "classification":
        st.subheader("Classification Results")
        if "category" in results:
            st.success(f"Category: {results['category']}")
        if "confidence" in results:
            st.metric("Confidence", f"{results['confidence']:.2f}")
    
    elif result_type == "translation":
        st.subheader("Translation Result")
        st.success(results.get("translated_text", "Translation failed"))
        if "source_language" in results:
            st.info(f"Detected source language: {results['source_language']}")
    
    elif result_type == "generation":
        st.subheader("Generated Text")
        st.write(results.get("generated_text", "Generation failed"))
    
    elif result_type == "summarization":
        st.subheader("Summary")
        st.write(results.get("summary", "Summarization failed"))
    
    elif result_type == "qa":
        st.subheader("Answer")
        st.success(results.get("answer", "No answer found"))
        if "confidence" in results:
            st.metric("Confidence", f"{results['confidence']:.2f}")

def handle_file_upload(uploaded_file):
    """
    Handle file upload and extract text content
    """
    if uploaded_file is not None:
        try:
            # Read file content
            if uploaded_file.type == "text/plain":
                content = str(uploaded_file.read(), "utf-8")
            else:
                st.error("Only text files (.txt) are supported for upload.")
                return None
            return content
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            return None
    return None

def validate_input(text: str, min_length: int = 1) -> bool:
    """
    Validate user input text
    """
    if not text or len(text.strip()) < min_length:
        return False
    return True

def create_download_link(content: str, filename: str, link_text: str):
    """
    Create a download link for text content
    """
    b64_content = pd.io.common.BytesIO()
    b64_content.write(content.encode())
    b64_content.seek(0)
    
    st.download_button(
        label=link_text,
        data=content,
        file_name=filename,
        mime="text/plain"
    )

def display_error(error_message: str, error_type: str = "error"):
    """
    Display error messages in a consistent format
    """
    if error_type == "error":
        st.error(f"❌ {error_message}")
    elif error_type == "warning":
        st.warning(f"⚠️ {error_message}")
    elif error_type == "info":
        st.info(f"ℹ️ {error_message}")

def format_processing_time(start_time, end_time):
    """
    Format and display processing time
    """
    processing_time = end_time - start_time
    st.caption(f"⏱️ Processing time: {processing_time:.2f} seconds")
                                                 
