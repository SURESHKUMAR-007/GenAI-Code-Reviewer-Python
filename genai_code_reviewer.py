import streamlit as st
import ast

def analyze_code(code):
    """
    This function simulates AI code review by checking for:
    1. Syntax Errors (Real Python checks)
    2. Code Style issues (Logic-based checks)
    """
    bugs = []
    suggestions = []
    
    # 1. Check for Syntax Errors using AST
    try:
        ast.parse(code)
    except SyntaxError as e:
        bugs.append(f"❌ Syntax Error: {e.msg} at line {e.lineno}")
        bugs.append(f"   *Fix:* Check your brackets, colons, or indentation at line {e.lineno}.")
        return bugs, suggestions # Stop analysis if syntax is wrong

    # 2. Logic-Based "AI" Checks (Simulating GenAI)
    
    # Check for empty exception handling
    if "except:" in code or "except Exception:" in code:
        if "pass" in code:
            bugs.append("⚠️ Potential Bug: Empty 'except' block detected.")
            suggestions.append("Avoid using 'pass' in exception blocks. Log the error or print a message so you know what went wrong.")

    # Check for Division by Zero risk
    if "/" in code and "if" not in code:
        bugs.append("⚠️ Risk: Potential Division by Zero.")
        suggestions.append("You are dividing numbers but not checking if the denominator is zero. Add an 'if' check.")

    # Check for using print() instead of return in functions
    if "def " in code and "print(" in code and "return" not in code:
        suggestions.append("💡 Improvement: This function prints a value but doesn't return it. Consider using 'return' so the data can be used elsewhere.")

    # Check for missing docstrings
    if "def " in code and '"""' not in code:
        suggestions.append("💡 Best Practice: Your function is missing a Docstring. Add a comment at the start to explain what it does.")

    # If no issues found
    if not bugs and not suggestions:
        suggestions.append("✅ Great Job! Your code looks clean and runs without syntax errors.")

    return bugs, suggestions

# --- Streamlit UI Code ---

st.set_page_config(page_title="GenAI Code Reviewer", page_icon="🤖")

st.title("🤖 GenAI Code Reviewer")
st.write("Submit your Python code below for an instant review (Powered by Logic AI).")

# Input text box
code_input = st.text_area("Paste your Python code here:", height=200)

if st.button("Generate Review"):
    if code_input.strip():
        with st.spinner("Analyzing code..."):
            # Call our local "AI" function
            bugs, suggestions = analyze_code(code_input)
            
            # Display Results
            st.subheader("📋 Review Report")
            
            # Show Bugs
            if bugs:
                st.error("### 🐞 Bugs Found")
                for bug in bugs:
                    st.write(bug)
            else:
                st.success("No syntax errors found!")

            # Show Suggestions
            st.info("### 💡 Suggestions for Improvement")
            for suggestion in suggestions:
                st.write(f"- {suggestion}")

            # Show "Fixed" Code (A simple example of how it might look)
            st.subheader("✨ Optimized Code Snippet")
            st.code(code_input, language='python') 
            st.caption("Review the suggestions above to manually apply fixes.")
            
    else:
        st.warning("Please enter some code first.")
