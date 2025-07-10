"""
Text Generation Module
Generates text using simple templates and TextBlob for creative content
"""
import streamlit as st
from textblob import TextBlob
import random
from typing import Dict, Any, List

class TextGenerator:
    def __init__(self):
        self.story_templates = [
            "Once upon a time in {setting}, there lived a {character} who {action}.",
            "In the year {year}, {character} discovered {discovery} while {activity}.",
            "The {adjective} {character} decided to {action} despite the {obstacle}.",
            "Every morning, {character} would {routine} before {main_activity}."
        ]
        
        self.email_templates = {
            "professional": "Dear {recipient},\n\nI hope this email finds you well. I am writing to {purpose}. {details}\n\nBest regards,\n{sender}",
            "casual": "Hi {recipient}!\n\n{greeting} I wanted to {purpose}. {details}\n\nTalk soon,\n{sender}",
            "formal": "Dear {recipient},\n\nI am writing to formally {purpose}. {details}\n\nSincerely,\n{sender}"
        }
        
        self.blog_templates = [
            "# {title}\n\n{intro}\n\n## Main Points\n\n{content}\n\n## Conclusion\n\n{conclusion}",
            "# {title}\n\n{hook}\n\n{content}\n\n**Key Takeaways:**\n- {takeaway1}\n- {takeaway2}\n- {takeaway3}"
        ]
        
        # Word banks for template filling
        self.word_banks = {
            "settings": ["a distant galaxy", "ancient Rome", "modern Tokyo", "a small village", "the deep ocean", "a magical forest"],
            "characters": ["brave knight", "curious scientist", "young artist", "wise elder", "mysterious stranger", "talented musician"],
            "actions": ["embarked on an adventure", "made an important discovery", "faced their greatest fear", "learned a valuable lesson"],
            "adjectives": ["determined", "creative", "ambitious", "thoughtful", "innovative", "passionate"],
            "years": ["2025", "2030", "2040", "3025", "1995", "2050"],
            "discoveries": ["a hidden treasure", "ancient wisdom", "new technology", "a secret passage", "magical powers"],
            "activities": ["exploring caves", "reading old books", "experimenting in the lab", "traveling the world"],
            "obstacles": ["terrible storm", "lack of resources", "fierce competition", "personal doubts"],
            "routines": ["meditate quietly", "practice their craft", "study ancient texts", "exercise vigorously"]
        }
    
    def generate_story(self, theme: str = "", length: str = "short") -> Dict[str, Any]:
        """
        Generate a creative story based on theme and length
        """
        try:
            template = random.choice(self.story_templates)
            
            # Fill template with random words
            story = template.format(
                setting=random.choice(self.word_banks["settings"]),
                character=random.choice(self.word_banks["characters"]),
                action=random.choice(self.word_banks["actions"]),
                year=random.choice(self.word_banks["years"]),
                discovery=random.choice(self.word_banks["discoveries"]),
                activity=random.choice(self.word_banks["activities"]),
                adjective=random.choice(self.word_banks["adjectives"]),
                obstacle=random.choice(self.word_banks["obstacles"]),
                routine=random.choice(self.word_banks["routines"]),
                main_activity=random.choice(self.word_banks["activities"])
            )
            
            # Extend story based on length
            if length == "medium":
                extension = f" This led to {random.choice(['unexpected consequences', 'new friendships', 'great success', 'valuable lessons'])}."
                story += extension
            elif length == "long":
                extension1 = f" This led to {random.choice(['unexpected consequences', 'new friendships', 'great success', 'valuable lessons'])}."
                extension2 = f" Eventually, they {random.choice(['achieved their goal', 'found peace', 'inspired others', 'discovered their true purpose'])}."
                story += extension1 + extension2
            
            # Add theme if provided
            if theme:
                story = f"[Theme: {theme}] " + story
            
            return {
                "generated_text": story,
                "word_count": len(story.split()),
                "character_count": len(story),
                "type": "story"
            }
            
        except Exception as e:
            return {"error": f"Story generation failed: {str(e)}"}
    
    def generate_email(self, style: str, purpose: str, recipient: str = "Recipient", sender: str = "Sender") -> Dict[str, Any]:
        """
        Generate an email based on style and purpose
        """
        try:
            template = self.email_templates.get(style, self.email_templates["professional"])
            
            # Generate content based on purpose
            if "meeting" in purpose.lower():
                details = "I would like to schedule a meeting to discuss this matter further. Please let me know your availability."
                greeting = "Hope you're having a great day!"
            elif "follow" in purpose.lower():
                details = "I wanted to follow up on our previous conversation and see if you had any questions."
                greeting = "Hope you're doing well!"
            elif "thank" in purpose.lower():
                details = "I wanted to express my sincere gratitude for your time and assistance."
                greeting = "Hope this finds you well!"
            else:
                details = "I look forward to your response and any feedback you might have."
                greeting = "Hope you're having a wonderful day!"
            
            email = template.format(
                recipient=recipient,
                sender=sender,
                purpose=purpose,
                details=details,
                greeting=greeting
            )
            
            return {
                "generated_text": email,
                "word_count": len(email.split()),
                "character_count": len(email),
                "type": "email"
            }
            
        except Exception as e:
            return {"error": f"Email generation failed: {str(e)}"}
    
    def generate_blog_post(self, title: str, main_points: List[str]) -> Dict[str, Any]:
        """
        Generate a blog post based on title and main points
        """
        try:
            template = random.choice(self.blog_templates)
            
            # Generate intro
            intro = f"In this post, we'll explore {title.lower()} and discuss why it matters in today's world."
            
            # Generate content from main points
            content = "\n\n".join([f"### {point}\n\nThis is an important aspect that deserves careful consideration." for point in main_points])
            
            # Generate conclusion
            conclusion = "In summary, these insights can help guide future decisions and actions."
            
            # Generate takeaways
            takeaways = main_points[:3] if len(main_points) >= 3 else main_points + ["Consider the broader implications"] * (3 - len(main_points))
            
            blog_post = template.format(
                title=title,
                intro=intro,
                content=content,
                conclusion=conclusion,
                hook="Have you ever wondered about this topic?",
                takeaway1=takeaways[0],
                takeaway2=takeaways[1],
                takeaway3=takeaways[2]
            )
            
            return {
                "generated_text": blog_post,
                "word_count": len(blog_post.split()),
                "character_count": len(blog_post),
                "type": "blog_post"
            }
            
        except Exception as e:
            return {"error": f"Blog post generation failed: {str(e)}"}
    
    def continue_text(self, input_text: str, style: str = "creative") -> Dict[str, Any]:
        """
        Continue existing text based on context and style
        """
        try:
            blob = TextBlob(input_text)
            
            # Analyze the input text for context
            last_sentence = str(blob.sentences[-1]) if blob.sentences else input_text
            
            # Generate continuation based on style
            if style == "creative":
                continuations = [
                    " This sparked a new idea that would change everything.",
                    " Little did they know, this was just the beginning.",
                    " The implications of this were far-reaching.",
                    " Something unexpected was about to happen.",
                    " This moment would be remembered for years to come."
                ]
            elif style == "informative":
                continuations = [
                    " Research shows that this approach has several benefits.",
                    " It's important to consider the following factors.",
                    " This concept can be applied in various contexts.",
                    " Further analysis reveals additional insights.",
                    " These findings suggest new possibilities."
                ]
            elif style == "conversational":
                continuations = [
                    " You might be wondering what happened next.",
                    " I think you'll find this interesting.",
                    " This reminds me of something similar.",
                    " Here's what I learned from this experience.",
                    " Let me tell you what happened after that."
                ]
            else:
                continuations = [
                    " This leads to several important considerations.",
                    " The next step involves careful planning.",
                    " These developments warrant further attention.",
                    " Such circumstances require thoughtful analysis."
                ]
            
            continuation = random.choice(continuations)
            continued_text = input_text + continuation
            
            return {
                "generated_text": continued_text,
                "original_length": len(input_text.split()),
                "new_length": len(continued_text.split()),
                "added_text": continuation,
                "type": "continuation"
            }
            
        except Exception as e:
            return {"error": f"Text continuation failed: {str(e)}"}

# Streamlit interface for text generation
def create_text_generation_interface():
    """
    Create the Streamlit interface for text generation
    """
    st.header("✍️ Text Generation")
    st.write("Generate creative content including stories, emails, blog posts, and text continuations.")
    
    generator = TextGenerator()
    
    # Generation type selection
    gen_type = st.selectbox(
        "Choose generation type:",
        ["Story Generation", "Email Writing", "Blog Post Creation", "Text Continuation"]
    )
    
    if gen_type == "Story Generation":
        st.subheader("📚 Story Generator")
        
        col1, col2 = st.columns(2)
        with col1:
            theme = st.text_input("Theme (optional):", placeholder="e.g., friendship, adventure, mystery")
        with col2:
            length = st.selectbox("Story length:", ["short", "medium", "long"])
        
        if st.button("Generate Story", type="primary"):
            with st.spinner("Creating your story..."):
                result = generator.generate_story(theme, length)
                
                if "error" not in result:
                    st.subheader("Generated Story")
                    st.write(result["generated_text"])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Words", result["word_count"])
                    with col2:
                        st.metric("Characters", result["character_count"])
                    
                    from utils.helpers import create_download_link
                    create_download_link(
                        result["generated_text"],
                        "generated_story.txt",
                        "📥 Download Story"
                    )
                else:
                    from utils.helpers import display_error
                    display_error(result["error"])
    
    elif gen_type == "Email Writing":
        st.subheader("📧 Email Generator")
        
        col1, col2 = st.columns(2)
        with col1:
            style = st.selectbox("Email style:", ["professional", "casual", "formal"])
            recipient = st.text_input("Recipient name:", value="Recipient")
        with col2:
            sender = st.text_input("Your name:", value="Your Name")
            purpose = st.text_input("Email purpose:", placeholder="e.g., schedule a meeting, follow up, thank you")
        
        if st.button("Generate Email", type="primary"):
            if purpose:
                with st.spinner("Writing your email..."):
                    result = generator.generate_email(style, purpose, recipient, sender)
                    
                    if "error" not in result:
                        st.subheader("Generated Email")
                        st.code(result["generated_text"], language="text")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Words", result["word_count"])
                        with col2:
                            st.metric("Characters", result["character_count"])
                        
                        from utils.helpers import create_download_link
                        create_download_link(
                            result["generated_text"],
                            "generated_email.txt",
                            "📥 Download Email"
                        )
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
            else:
                from utils.helpers import display_error
                display_error("Please specify the email purpose.")
    
    elif gen_type == "Blog Post Creation":
        st.subheader("📝 Blog Post Generator")
        
        title = st.text_input("Blog post title:", placeholder="e.g., The Future of Technology")
        
        st.write("Main points to cover:")
        num_points = st.slider("Number of main points:", 1, 5, 3)
        
        main_points = []
        for i in range(num_points):
            point = st.text_input(f"Point {i+1}:", placeholder=f"Main point {i+1}", key=f"point_{i}")
            if point:
                main_points.append(point)
        
        if st.button("Generate Blog Post", type="primary"):
            if title and main_points:
                with st.spinner("Creating your blog post..."):
                    result = generator.generate_blog_post(title, main_points)
                    
                    if "error" not in result:
                        st.subheader("Generated Blog Post")
                        st.markdown(result["generated_text"])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Words", result["word_count"])
                        with col2:
                            st.metric("Characters", result["character_count"])
                        
                        from utils.helpers import create_download_link
                        create_download_link(
                            result["generated_text"],
                            "generated_blog_post.md",
                            "📥 Download Blog Post"
                        )
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
            else:
                from utils.helpers import display_error
                display_error("Please provide a title and at least one main point.")
    
    elif gen_type == "Text Continuation":
        st.subheader("🔄 Text Continuation")
        
        input_text = st.text_area(
            "Enter text to continue:",
            height=150,
            placeholder="Start writing something and I'll continue it for you..."
        )
        
        style = st.selectbox(
            "Continuation style:",
            ["creative", "informative", "conversational", "formal"]
        )
        
        if st.button("Continue Text", type="primary"):
            if input_text and len(input_text.strip()) > 10:
                with st.spinner("Continuing your text..."):
                    result = generator.continue_text(input_text, style)
                    
                    if "error" not in result:
                        st.subheader("Continued Text")
                        st.write(result["generated_text"])
                        
                        st.subheader("Added Text")
                        st.info(result["added_text"])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Original Words", result["original_length"])
                        with col2:
                            st.metric("Total Words", result["new_length"])
                        
                        from utils.helpers import create_download_link
                        create_download_link(
                            result["generated_text"],
                            "continued_text.txt",
                            "📥 Download Continued Text"
                        )
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
            else:
                from utils.helpers import display_error
                display_error("Please enter at least 10 characters of text to continue.")

if __name__ == "__main__":
    import pandas as pd
    create_text_generation_interface()
                      
