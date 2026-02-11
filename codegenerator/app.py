"""
AI Code Generator - Streamlit App
Generate, explain, debug, and optimize code using OpenAI GPT
"""

import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Code Generator",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        max-width: 1400px;
        margin: 0 auto;
    }
    .code-output {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4CAF50;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = ""
if 'history' not in st.session_state:
    st.session_state.history = []

# Helper function
def get_file_extension(language):
    """Get file extension for programming language"""
    extensions = {
        "Python": "py",
        "JavaScript": "js",
        "TypeScript": "ts",
        "Java": "java",
        "C++": "cpp",
        "C#": "cs",
        "Go": "go",
        "Rust": "rs",
        "PHP": "php",
        "Ruby": "rb",
        "Swift": "swift",
        "Kotlin": "kt",
        "R": "r",
        "SQL": "sql",
        "HTML/CSS": "html",
        "Shell/Bash": "sh"
    }
    return extensions.get(language, "txt")

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    # API Key input
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        help="Enter your OpenAI API key or set OPENAI_API_KEY environment variable"
    )
    
    st.markdown("---")
    
    # Model selection
    model = st.selectbox(
        "Model",
        ["gpt-4", "gpt-3.5-turbo"],
        help="GPT-4 is more capable but slower and more expensive"
    )
    
    # Temperature
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more creative, lower values more deterministic"
    )
    
    # Max tokens
    max_tokens = st.slider(
        "Max Tokens",
        min_value=256,
        max_value=4000,
        value=2000,
        step=256,
        help="Maximum length of generated code"
    )
    
    st.markdown("---")
    
    # History
    st.subheader("📜 History")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"{item['language']} - {item['task'][:30]}..."):
                st.caption(item['prompt'][:100] + "...")
    else:
        st.caption("No history yet")
    
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()
    
    st.markdown("---")
    
    # Info
    st.markdown("### 💡 Tips")
    st.caption("""
    - Be specific in your descriptions
    - Include input/output examples
    - Mention frameworks or libraries
    - Specify edge cases
    """)
    
    st.markdown("---")
    st.caption("Built with Streamlit & OpenAI")

# Main content
st.title("💻 AI Code Generator")
st.markdown("Generate, explain, debug, and optimize code using AI")

# Check API key
if not api_key:
    st.warning("⚠️ Please enter your OpenAI API key in the sidebar to get started")
    st.info("""
    **How to get an API key:**
    1. Go to https://platform.openai.com/api-keys
    2. Sign up or log in
    3. Create a new API key
    4. Copy and paste it in the sidebar
    """)
    st.stop()

# Initialize OpenAI client
try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    st.error(f"Error initializing OpenAI client: {e}")
    st.stop()

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    # Language selection
    language = st.selectbox(
        "Programming Language",
        [
            "Python", "JavaScript", "TypeScript", "Java", "C++", "C#",
            "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin", "R",
            "SQL", "HTML/CSS", "Shell/Bash", "Other"
        ]
    )

with col2:
    # Task type
    task_type = st.selectbox(
        "Task Type",
        [
            "Generate Code",
            "Explain Code",
            "Debug Code",
            "Optimize Code",
            "Add Documentation",
            "Convert Language",
            "Write Tests"
        ]
    )

# Input area
st.markdown("### 📝 Your Request")

if task_type in ["Explain Code", "Debug Code", "Optimize Code", "Add Documentation"]:
    # For tasks that need existing code
    col_prompt, col_code = st.columns([1, 1])
    
    with col_prompt:
        user_prompt = st.text_area(
            "Description",
            placeholder="Describe what you want to do with the code...",
            height=150
        )
    
    with col_code:
        existing_code = st.text_area(
            "Existing Code",
            placeholder="Paste your code here...",
            height=150
        )
else:
    # For code generation
    user_prompt = st.text_area(
        "Describe what you want to create",
        placeholder="Example: Create a function to calculate the factorial of a number recursively",
        height=150
    )
    existing_code = ""

# Additional options
with st.expander("⚙️ Advanced Options"):
    col_a, col_b = st.columns(2)
    
    with col_a:
        include_comments = st.checkbox("Include comments", value=True)
        include_examples = st.checkbox("Include usage examples", value=False)
    
    with col_b:
        include_tests = st.checkbox("Include unit tests", value=False)
        follow_best_practices = st.checkbox("Follow best practices", value=True)

# Generate button
generate_button = st.button("🚀 Generate", type="primary", use_container_width=True)

# Generate code
if generate_button:
    if not user_prompt:
        st.error("Please provide a description of what you want")
    else:
        with st.spinner("Generating code... This may take a few seconds..."):
            try:
                # Build the prompt
                system_prompt = f"""You are an expert {language} programmer. 
Your task is to help with: {task_type}.
{"Include detailed comments in the code." if include_comments else ""}
{"Include usage examples." if include_examples else ""}
{"Include unit tests." if include_tests else ""}
{"Follow best practices and coding standards." if follow_best_practices else ""}
Provide clean, efficient, and well-structured code."""

                user_message = user_prompt
                if existing_code:
                    user_message += f"\n\nExisting code:\n```{language.lower()}\n{existing_code}\n```"
                
                # Call OpenAI API
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                generated_code = response.choices[0].message.content
                st.session_state.generated_code = generated_code
                
                # Add to history
                st.session_state.history.append({
                    'language': language,
                    'task': task_type,
                    'prompt': user_prompt,
                    'code': generated_code
                })
                
                st.success("✅ Code generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Error generating code: {str(e)}")
                st.info("Please check your API key and try again")

# Display generated code
if st.session_state.generated_code:
    st.markdown("### 📄 Generated Code")
    
    # Action buttons
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    
    with col_btn1:
        if st.button("📋 Copy to Clipboard"):
            st.code(st.session_state.generated_code, language=language.lower())
            st.info("Code displayed above - use your browser's copy function")
    
    with col_btn2:
        st.download_button(
            label="💾 Download",
            data=st.session_state.generated_code,
            file_name=f"generated_code.{get_file_extension(language)}",
            mime="text/plain"
        )
    
    with col_btn3:
        if st.button("🔄 Regenerate"):
            st.rerun()
    
    with col_btn4:
        if st.button("🗑️ Clear"):
            st.session_state.generated_code = ""
            st.rerun()
    
    # Display code with syntax highlighting
    st.code(st.session_state.generated_code, language=language.lower())
    
    # Token usage info
    st.caption(f"Model: {model} | Temperature: {temperature}")

# Example prompts
with st.expander("💡 Example Prompts"):
    st.markdown("""
    **Generate Code:**
    - Create a REST API endpoint for user authentication in Express.js
    - Write a Python function to merge two sorted lists
    - Build a React component for a todo list with add/delete functionality
    
    **Explain Code:**
    - Explain how this recursive function works
    - What does this regex pattern match?
    - Break down this SQL query step by step
    
    **Debug Code:**
    - Fix the syntax errors in this code
    - Why is this function returning undefined?
    - Find the bug causing the infinite loop
    
    **Optimize Code:**
    - Improve the time complexity of this algorithm
    - Reduce memory usage in this function
    - Make this database query more efficient
    """)

# Footer
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.metric("Languages Supported", "15+")

with col_f2:
    st.metric("Task Types", "7")

with col_f3:
    if st.session_state.history:
        st.metric("Generations", len(st.session_state.history))
    else:
        st.metric("Generations", "0")
