"""
Named Entity Recognition Module
Extracts and classifies named entities from text using spaCy and NLTK
"""
import streamlit as st
import re
import pandas as pd
from textblob import TextBlob
from typing import Dict, Any, List, Tuple
from collections import Counter
import nltk

# Download required NLTK data
try:
    nltk.data.find('maxent_ne_chunker')
except LookupError:
    nltk.download('maxent_ne_chunker', quiet=True)

try:
    nltk.data.find('words')
except LookupError:
    nltk.download('words', quiet=True)

try:
    nltk.data.find('averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger', quiet=True)

from nltk import ne_chunk, pos_tag, word_tokenize

class NERExtractor:
    def __init__(self):
        # Entity patterns for rule-based extraction
        self.entity_patterns = {
            'PERSON': [
                r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # First Last
                r'\b(?:Mr|Mrs|Ms|Dr|Prof)\. [A-Z][a-z]+\b',  # Title + Name
                r'\b[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+\b'  # First M. Last
            ],
            'ORGANIZATION': [
                r'\b[A-Z][a-z]+ (?:Inc|Corp|LLC|Ltd|Company|Corporation|Group|Institute|University)\b',
                r'\b(?:Microsoft|Google|Apple|Amazon|Facebook|Tesla|IBM|Intel|Oracle)\b',
                r'\b[A-Z][A-Z]+ [A-Z][a-z]+\b'  # Acronym + word
            ],
            'LOCATION': [
                r'\b[A-Z][a-z]+ (?:City|State|Country|Street|Avenue|Road|Boulevard|Drive|Lane)\b',
                r'\b(?:New York|Los Angeles|Chicago|Houston|Phoenix|Philadelphia|San Antonio|San Diego|Dallas|San Jose)\b',
                r'\b(?:California|Texas|Florida|New York|Pennsylvania|Illinois|Ohio|Georgia|North Carolina|Michigan)\b',
                r'\b(?:USA|United States|UK|United Kingdom|Canada|Australia|Germany|France|Japan|China)\b'
            ],
            'DATE': [
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
                r'\b\d{1,2}/\d{1,2}/\d{4}\b',
                r'\b\d{4}-\d{2}-\d{2}\b',
                r'\b(?:19|20)\d{2}\b'
            ],
            'TIME': [
                r'\b\d{1,2}:\d{2}(?:\s*(?:AM|PM|am|pm))?\b',
                r'\b(?:morning|afternoon|evening|night|noon|midnight)\b'
            ],
            'MONEY': [
                r'\$\d+(?:,\d{3})*(?:\.\d{2})?\b',
                r'\b\d+(?:,\d{3})*\s*(?:dollars?|USD|cents?)\b',
                r'\b(?:€|£|¥)\d+(?:,\d{3})*(?:\.\d{2})?\b'
            ],
            'EMAIL': [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            ],
            'PHONE': [
                r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',
                r'\b\d{3}-\d{3}-\d{4}\b'
            ],
            'URL': [
                r'https?://[^\s<>"]+|www\.[^\s<>"]+\.[^\s<>"]+',
                r'\b[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:/[^\s]*)?\b'
            ]
        }
        
        # Common titles and prefixes
        self.person_titles = {'Mr', 'Mrs', 'Ms', 'Dr', 'Prof', 'Sir', 'Madam', 'Captain', 'Major', 'Colonel'}
        self.org_suffixes = {'Inc', 'Corp', 'LLC', 'Ltd', 'Company', 'Corporation', 'Group', 'Institute', 'University', 'College'}
    
    def extract_entities_rule_based(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract entities using rule-based pattern matching
        """
        entities = {}
        
        for entity_type, patterns in self.entity_patterns.items():
            entities[entity_type] = []
            
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    entity_text = match.group()
                    start_pos = match.start()
                    end_pos = match.end()
                    
                    # Avoid duplicates
                    if not any(e['text'].lower() == entity_text.lower() for e in entities[entity_type]):
                        entities[entity_type].append({
                            'text': entity_text,
                            'start': start_pos,
                            'end': end_pos,
                            'confidence': 0.8  # Rule-based confidence
                        })
        
        return entities
    
    def extract_entities_nltk(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract entities using NLTK's named entity recognition
        """
        try:
            # Tokenize and tag
            tokens = word_tokenize(text)
            pos_tags = pos_tag(tokens)
            
            # Named entity chunking
            tree = ne_chunk(pos_tags)
            
            entities = {
                'PERSON': [],
                'ORGANIZATION': [],
                'LOCATION': [],
                'GPE': [],  # Geopolitical entity
                'GSP': []   # Geographic/Social/Political
            }
            
            current_entity = []
            current_label = None
            
            for subtree in tree:
                if hasattr(subtree, 'label'):
                    # This is a named entity
                    entity_name = ' '.join([token for token, pos in subtree.leaves()])
                    entity_label = subtree.label()
                    
                    # Map NLTK labels to our standard labels
                    if entity_label in ['PERSON']:
                        mapped_label = 'PERSON'
                    elif entity_label in ['ORGANIZATION']:
                        mapped_label = 'ORGANIZATION'
                    elif entity_label in ['GPE', 'GSP']:
                        mapped_label = 'LOCATION'
                    else:
                        mapped_label = entity_label
                    
                    if mapped_label in entities:
                        entities[mapped_label].append({
                            'text': entity_name,
                            'start': 0,  # NLTK doesn't provide position info easily
                            'end': len(entity_name),
                            'confidence': 0.7  # NLTK confidence
                        })
            
            return entities
            
        except Exception as e:
            st.warning(f"NLTK NER failed: {str(e)}")
            return {}
    
    def extract_entities_comprehensive(self, text: str) -> Dict[str, Any]:
        """
        Comprehensive entity extraction combining multiple approaches
        """
        try:
            if not text or len(text.strip()) < 10:
                return {"error": "Text too short for entity extraction"}
            
            # Rule-based extraction
            rule_entities = self.extract_entities_rule_based(text)
            
            # NLTK extraction
            nltk_entities = self.extract_entities_nltk(text)
            
            # Combine and deduplicate entities
            combined_entities = {}
            
            for entity_type in ['PERSON', 'ORGANIZATION', 'LOCATION', 'DATE', 'TIME', 'MONEY', 'EMAIL', 'PHONE', 'URL']:
                combined_entities[entity_type] = []
                
                # Add rule-based entities
                if entity_type in rule_entities:
                    combined_entities[entity_type].extend(rule_entities[entity_type])
                
                # Add NLTK entities (avoid duplicates)
                if entity_type in nltk_entities:
                    for nltk_entity in nltk_entities[entity_type]:
                        if not any(
                            e['text'].lower() == nltk_entity['text'].lower() 
                            for e in combined_entities[entity_type]
                        ):
                            combined_entities[entity_type].append(nltk_entity)
            
            # Calculate statistics
            total_entities = sum(len(entities) for entities in combined_entities.values())
            entity_counts = {
                entity_type: len(entities) 
                for entity_type, entities in combined_entities.items()
            }
            
            # Find most common entities
            all_entity_texts = []
            for entities in combined_entities.values():
                all_entity_texts.extend([e['text'] for e in entities])
            
            most_common = Counter(all_entity_texts).most_common(10)
            
            return {
                'entities': combined_entities,
                'total_entities': total_entities,
                'entity_counts': entity_counts,
                'most_common_entities': most_common,
                'text_length': len(text),
                'processing_method': 'Combined (Rule-based + NLTK)'
            }
            
        except Exception as e:
            return {"error": f"Entity extraction failed: {str(e)}"}
    
    def analyze_entity_relationships(self, entities: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Analyze relationships between extracted entities
        """
        try:
            relationships = []
            
            # Find co-occurring entities (simple proximity-based relationships)
            persons = entities.get('PERSON', [])
            organizations = entities.get('ORGANIZATION', [])
            locations = entities.get('LOCATION', [])
            
            # Person-Organization relationships
            for person in persons:
                for org in organizations:
                    relationships.append({
                        'type': 'PERSON-ORGANIZATION',
                        'entity1': person['text'],
                        'entity2': org['text'],
                        'relationship': 'associated_with'
                    })
            
            # Person-Location relationships
            for person in persons:
                for location in locations:
                    relationships.append({
                        'type': 'PERSON-LOCATION',
                        'entity1': person['text'],
                        'entity2': location['text'],
                        'relationship': 'located_in'
                    })
            
            # Organization-Location relationships
            for org in organizations:
                for location in locations:
                    relationships.append({
                        'type': 'ORGANIZATION-LOCATION',
                        'entity1': org['text'],
                        'entity2': location['text'],
                        'relationship': 'based_in'
                    })
            
            return {
                'relationships': relationships,
                'relationship_count': len(relationships),
                'relationship_types': list(set(r['type'] for r in relationships))
            }
            
        except Exception as e:
            return {"error": f"Relationship analysis failed: {str(e)}"}
    
    def extract_custom_patterns(self, text: str, custom_patterns: Dict[str, str]) -> Dict[str, List[str]]:
        """
        Extract entities based on custom user-defined patterns
        """
        try:
            custom_entities = {}
            
            for pattern_name, pattern in custom_patterns.items():
                matches = re.findall(pattern, text, re.IGNORECASE)
                custom_entities[pattern_name] = list(set(matches))  # Remove duplicates
            
            return custom_entities
            
        except Exception as e:
            return {"error": f"Custom pattern extraction failed: {str(e)}"}
    
    def batch_extract_entities(self, texts: List[str]) -> Dict[str, Any]:
        """
        Extract entities from multiple texts in batch
        """
        try:
            batch_results = []
            
            for i, text in enumerate(texts):
                if text and len(text.strip()) > 5:
                    result = self.extract_entities_comprehensive(text)
                    
                    if "error" not in result:
                        batch_results.append({
                            'text_id': i + 1,
                            'text_preview': text[:100] + "..." if len(text) > 100 else text,
                            'total_entities': result['total_entities'],
                            'entity_counts': result['entity_counts'],
                            'entities': result['entities']
                        })
            
            # Aggregate statistics
            total_texts = len(batch_results)
            total_entities_all = sum(r['total_entities'] for r in batch_results)
            avg_entities_per_text = total_entities_all / total_texts if total_texts > 0 else 0
            
            # Combine entity counts
            combined_counts = {}
            for result in batch_results:
                for entity_type, count in result['entity_counts'].items():
                    combined_counts[entity_type] = combined_counts.get(entity_type, 0) + count
            
            return {
                'batch_results': batch_results,
                'total_texts': total_texts,
                'total_entities': total_entities_all,
                'average_entities_per_text': avg_entities_per_text,
                'combined_entity_counts': combined_counts
            }
            
        except Exception as e:
            return {"error": f"Batch entity extraction failed: {str(e)}"}

# Streamlit interface for named entity recognition
def create_ner_interface():
    """
    Create the Streamlit interface for named entity recognition
    """
    st.header("🏷️ Named Entity Recognition")
    st.write("Extract and identify people, organizations, locations, dates, and other entities from your text.")
    
    ner_extractor = NERExtractor()
    
    # NER mode selection
    ner_mode = st.selectbox(
        "Choose NER mode:",
        ["Single Text Analysis", "Batch Text Analysis", "Custom Pattern Extraction", "Entity Relationships"]
    )
    
    if ner_mode == "Single Text Analysis":
        st.subheader("📝 Single Text Entity Extraction")
        
        # Input options
        input_method = st.radio("Choose input method:", ["Text Input", "File Upload"])
        
        text_to_analyze = ""
        
        if input_method == "Text Input":
            text_to_analyze = st.text_area(
                "Enter text to analyze:",
                height=200,
                placeholder="Paste your text here to extract named entities..."
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload a text file:",
                type=['txt'],
                help="Upload a .txt file for entity extraction"
            )
            if uploaded_file:
                from utils.helpers import handle_file_upload
                text_to_analyze = handle_file_upload(uploaded_file)
        
        if st.button("Extract Entities", type="primary"):
            if text_to_analyze and len(text_to_analyze.strip()) > 10:
                with st.spinner("Extracting entities..."):
                    result = ner_extractor.extract_entities_comprehensive(text_to_analyze)
                    
                    if "error" not in result:
                        # Summary statistics
                        st.subheader("📊 Entity Summary")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Total Entities", result["total_entities"])
                        with col2:
                            st.metric("Entity Types", len([t for t, c in result["entity_counts"].items() if c > 0]))
                        with col3:
                            st.metric("Text Length", f"{result['text_length']} chars")
                        
                        # Entity breakdown
                        st.subheader("🏷️ Entity Breakdown")
                        
                        # Create tabs for different entity types
                        entity_types = [t for t, entities in result["entities"].items() if len(entities) > 0]
                        
                        if entity_types:
                            entity_tabs = st.tabs(entity_types)
                            
                            for i, entity_type in enumerate(entity_types):
                                with entity_tabs[i]:
                                    entities = result["entities"][entity_type]
                                    
                                    st.write(f"**Found {len(entities)} {entity_type.lower()} entities:**")
                                    
                                    # Display entities in a nice format
                                    for j, entity in enumerate(entities, 1):
                                        col1, col2 = st.columns([3, 1])
                                        with col1:
                                            st.write(f"{j}. **{entity['text']}**")
                                        with col2:
                                            confidence_color = "🟢" if entity['confidence'] > 0.7 else "🟡" if entity['confidence'] > 0.5 else "🔴"
                                            st.write(f"{confidence_color} {entity['confidence']:.1%}")
                        else:
                            st.info("No named entities found in the text.")
                        
                        # Most common entities
                        if result["most_common_entities"]:
                            st.subheader("🔝 Most Common Entities")
                            common_df = pd.DataFrame(
                                result["most_common_entities"], 
                                columns=["Entity", "Frequency"]
                            )
                            st.dataframe(common_df, use_container_width=True)
                        
                        # Entity counts visualization
                        st.subheader("📈 Entity Distribution")
                        counts_df = pd.DataFrame([
                            {"Entity Type": entity_type, "Count": count}
                            for entity_type, count in result["entity_counts"].items()
                            if count > 0
                        ])
                        
                        if not counts_df.empty:
                            st.bar_chart(counts_df.set_index("Entity Type"))
                        
                        # Download results
                        entities_text = "Named Entity Recognition Results\n\n"
                        for entity_type, entities in result["entities"].items():
                            if entities:
                                entities_text += f"{entity_type}:\n"
                                for entity in entities:
                                    entities_text += f"- {entity['text']} (confidence: {entity['confidence']:.1%})\n"
                                entities_text += "\n"
                        
                        from utils.helpers import create_download_link
                        create_download_link(
                            entities_text,
                            "extracted_entities.txt",
                            "📥 Download Entity Results"
                        )
                    
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
            else:
                from utils.helpers import display_error
                display_error("Please enter at least 10 characters of text for analysis.")
    
    elif ner_mode == "Batch Text Analysis":
        st.subheader("📚 Batch Entity Extraction")
        st.info("Extract entities from multiple texts at once.")
        
        # Input multiple texts
        num_texts = st.slider("Number of texts:", min_value=2, max_value=10, value=3)
        
        texts = []
        for i in range(num_texts):
            text = st.text_area(f"Text {i+1}:", height=100, key=f"batch_ner_{i}")
            if text:
                texts.append(text)
        
        if st.button("Extract All Entities", type="primary"):
            if len(texts) >= 1:
                with st.spinner(f"Processing {len(texts)} texts..."):
                    result = ner_extractor.batch_extract_entities(texts)
                    
                    if "error" not in result:
                        # Batch summary
                        st.subheader("📊 Batch Summary")
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Texts Processed", result["total_texts"])
                        with col2:
                            st.metric("Total Entities", result["total_entities"])
                        with col3:
                            st.metric("Avg per Text", f"{result['average_entities_per_text']:.1f}")
                        with col4:
                            entity_types = len([t for t, c in result["combined_entity_counts"].items() if c > 0])
                            st.metric("Entity Types", entity_types)
                        
                        # Combined entity distribution
                        st.subheader("📈 Combined Entity Distribution")
                        combined_df = pd.DataFrame([
                            {"Entity Type": entity_type, "Total Count": count}
                            for entity_type, count in result["combined_entity_counts"].items()
                            if count > 0
                        ])
                        
                        if not combined_df.empty:
                            st.bar_chart(combined_df.set_index("Entity Type"))
                        
                        # Individual results
                        st.subheader("📄 Individual Results")
                        
                        for batch_result in result["batch_results"]:
                            with st.expander(f"Text {batch_result['text_id']} ({batch_result['total_entities']} entities)"):
                                st.write("**Text Preview:**")
                                st.write(batch_result["text_preview"])
                                
                                st.write("**Entity Breakdown:**")
                                entity_breakdown = pd.DataFrame([
                                    {"Type": entity_type, "Count": count}
                                    for entity_type, count in batch_result["entity_counts"].items()
                                    if count > 0
                                ])
                                
                                if not entity_breakdown.empty:
                                    st.dataframe(entity_breakdown, use_container_width=True)
                                else:
                                    st.write("No entities found.")
                        
                        # Download batch results
                        batch_content = "Batch Entity Extraction Results\n\n"
                        for batch_result in result["batch_results"]:
                            batch_content += f"=== Text {batch_result['text_id']} ===\n"
                            batch_content += f"Preview: {batch_result['text_preview']}\n"
                            batch_content += f"Total entities: {batch_result['total_entities']}\n\n"
                            
                            for entity_type, entities in batch_result["entities"].items():
                                if entities:
                                    batch_content += f"{entity_type}:\n"
                                    for entity in entities:
                                        batch_content += f"- {entity['text']}\n"
                                    batch_content += "\n"
                            batch_content += "\n"
                        
                        from utils.helpers import create_download_link
                        create_download_link(
                            batch_content,
                            "batch_entity_results.txt",
                            "📥 Download Batch Results"
                        )
                    
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
            else:
                from utils.helpers import display_error
                display_error("Please enter at least one text for analysis.")
    
    elif ner_mode == "Custom Pattern Extraction":
        st.subheader("🎯 Custom Pattern Extraction")
        st.info("Define your own patterns to extract specific types of entities.")
        
        text_input = st.text_area(
            "Enter text to analyze:",
            height=150,
            placeholder="Enter your text here..."
        )
        
        st.write("**Define Custom Patterns:**")
        st.caption("Use regular expressions to define patterns for entity extraction.")
        
        # Custom pattern inputs
        num_patterns = st.slider("Number of custom patterns:", min_value=1, max_value=5, value=2)
        
        custom_patterns = {}
        for i in range(num_patterns):
            col1, col2 = st.columns(2)
            with col1:
                pattern_name = st.text_input(f"Pattern {i+1} Name:", key=f"pattern_name_{i}", placeholder="e.g., Product Codes")
            with col2:
                pattern_regex = st.text_input(f"Pattern {i+1} Regex:", key=f"pattern_regex_{i}", placeholder="e.g., [A-Z]{2}-\d{4}")
            
            if pattern_name and pattern_regex:
                custom_patterns[pattern_name] = pattern_regex
        
        # Predefined example patterns
        st.write("**Or use predefined examples:**")
        example_patterns = {
            "Credit Card Numbers": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            "Social Security Numbers": r'\b\d{3}-\d{2}-\d{4}\b',
            "Product Codes": r'\b[A-Z]{2,3}-\d{3,6}\b',
            "ISBN Numbers": r'\b(?:ISBN[-\s]?)?(?:97[89][-\s]?)?\d{1,5}[-\s]?\d{1,7}[-\s]?\d{1,6}[-\s]?[\dX]\b'
        }
        
        selected_examples = st.multiselect(
            "Select predefined patterns:",
            list(example_patterns.keys())
        )
        
        # Add selected examples to custom patterns
        for example in selected_examples:
            custom_patterns[example] = example_patterns[example]
        
        if st.button("Extract Custom Entities", type="primary"):
            if text_input and custom_patterns:
                with st.spinner("Extracting custom entities..."):
                    result = ner_extractor.extract_custom_patterns(text_input, custom_patterns)
                    
                    if "error" not in result:
                        st.subheader("🎯 Custom Entity Results")
                        
                        total_found = sum(len(entities) for entities in result.values())
                        st.metric("Total Custom Entities Found", total_found)
                        
                        if total_found > 0:
                            for pattern_name, entities in result.items():
                                if entities:
                                    st.write(f"**{pattern_name}:** {len(entities)} found")
                                    for entity in entities:
                                        st.write(f"- {entity}")
                                    st.write("")
                        else:
                            st.info("No entities found matching your custom patterns.")
                        
                        # Download custom results
                        if total_found > 0:
                            custom_content = "Custom Pattern Extraction Results\n\n"
                            for pattern_name, entities in result.items():
                                if entities:
                                    custom_content += f"{pattern_name}:\n"
                                    for entity in entities:
                                        custom_content += f"- {entity}\n"
                                    custom_content += "\n"
                            
                            from utils.helpers import create_download_link
                            create_download_link(
                                custom_content,
                                "custom_entities.txt",
                                "📥 Download Custom Results"
                            )
                    
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
            else:
                from utils.helpers import display_error
                display_error("Please enter text and define at least one custom pattern.")
    
    elif ner_mode == "Entity Relationships":
        st.subheader("🔗 Entity Relationship Analysis")
        st.info("Analyze relationships between different types of entities in your text.")
        
        text_input = st.text_area(
            "Enter text to analyze relationships:",
            height=180,
            placeholder="Enter text containing multiple entities..."
        )
        
        if st.button("Analyze Relationships", type="primary"):
            if text_input and len(text_input.strip()) > 20:
                with st.spinner("Analyzing entity relationships..."):
                    # First extract entities
                    entity_result = ner_extractor.extract_entities_comprehensive(text_input)
                    
                    if "error" not in entity_result:
                        # Analyze relationships
                        relationship_result = ner_extractor.analyze_entity_relationships(entity_result["entities"])
                        
                        if "error" not in relationship_result:
                            # Display entity summary
                            st.subheader("🏷️ Extracted Entities")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                persons = entity_result["entities"].get("PERSON", [])
                                st.metric("Persons", len(persons))
                                if persons:
                                    for person in persons[:3]:
                                        st.write(f"• {person['text']}")
                            
                            with col2:
                                orgs = entity_result["entities"].get("ORGANIZATION", [])
                                st.metric("Organizations", len(orgs))
                                if orgs:
                                    for org in orgs[:3]:
                                        st.write(f"• {org['text']}")
                            
                            with col3:
                                locations = entity_result["entities"].get("LOCATION", [])
                                st.metric("Locations", len(locations))
                                if locations:
                                    for location in locations[:3]:
                                        st.write(f"• {location['text']}")
                            
                            # Display relationships
                            st.subheader("🔗 Identified Relationships")
                            
                            if relationship_result["relationships"]:
                                st.metric("Total Relationships", relationship_result["relationship_count"])
                                
                                # Group relationships by type
                                relationship_types = {}
                                for rel in relationship_result["relationships"]:
                                    rel_type = rel["type"]
                                    if rel_type not in relationship_types:
                                        relationship_types[rel_type] = []
                                    relationship_types[rel_type].append(rel)
                                
                                # Display by type
                                for rel_type, rels in relationship_types.items():
                                    with st.expander(f"{rel_type} ({len(rels)} relationships)"):
                                        for rel in rels:
                                            st.write(f"• **{rel['entity1']}** {rel['relationship']} **{rel['entity2']}**")
                                
                                # Create relationship dataframe
                                rel_df = pd.DataFrame(relationship_result["relationships"])
                                
                                st.subheader("📊 Relationship Table")
                                st.dataframe(rel_df, use_container_width=True)
                                
                                # Download relationship analysis
                                rel_content = "Entity Relationship Analysis\n\n"
                                rel_content += "EXTRACTED ENTITIES:\n"
                                for entity_type, entities in entity_result["entities"].items():
                                    if entities:
                                        rel_content += f"\n{entity_type}:\n"
                                        for entity in entities:
                                            rel_content += f"- {entity['text']}\n"
                                
                                rel_content += "\n\nIDENTIFIED RELATIONSHIPS:\n"
                                for rel in relationship_result["relationships"]:
                                    rel_content += f"- {rel['entity1']} {rel['relationship']} {rel['entity2']} ({rel['type']})\n"
                                
                                from utils.helpers import create_download_link
                                create_download_link(
                                    rel_content,
                                    "entity_relationships.txt",
                                    "📥 Download Relationship Analysis"
                                )
                            else:
                                st.info("No relationships could be identified between the extracted entities.")
                        
                        else:
                            from utils.helpers import display_error
                            display_error(relationship_result["error"])
                    
                    else:
                        from utils.helpers import display_error
                        display_error(entity_result["error"])
            else:
                from utils.helpers import display_error
                display_error("Please enter at least 20 characters of text for relationship analysis.")

if __name__ == "__main__":
    create_ner_interface()
