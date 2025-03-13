"""
NFA to DFA Converter Web Application.

This Streamlit application provides a user interface for:
1. Uploading NFA diagrams
2. Analyzing them with AI
3. Converting NFAs to DFAs
4. Visualizing the results
"""

import streamlit as st
from src.python.ai import AutomataAnalyzer
import os

def main():
    """
    Main function to run the Streamlit application.
    
    This function sets up the UI and handles the workflow for:
    - Uploading NFA diagrams
    - Analyzing them with AI
    - Converting NFAs to DFAs
    - Visualizing the results
    """
    # Set the page configuration with a new title
    st.set_page_config(page_title="NFA-DFA")  # Updated tab name
    st.title("Automata Converter")
    
    # Initialize session state
    if 'current_step' not in st.session_state:
        st.session_state.update({
            'current_step': 0,
            'uploaded_file': None,
            'analysis_result': None,
            'edited_result': None
        })

    # Step 0: File Upload
    if st.session_state.current_step == 0:
        st.subheader("Step 1: Upload State Diagram")
        uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        
        if uploaded_file:
            st.session_state.uploaded_file = uploaded_file
            st.image(uploaded_file, caption="Uploaded Diagram", use_container_width=True)
            
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("Next →", type="primary", use_container_width=True):
                    st.session_state.current_step = 1
                    st.rerun()

    # Step 1: Analysis Results
    elif st.session_state.current_step == 1:
        st.subheader("Step 2: Analysis Results")
        
        
        if st.session_state.uploaded_file:
            st.image(st.session_state.uploaded_file, caption="Your Diagram", use_container_width=True)
            
            api_key = st.secrets.get("MISTRAL_API_KEY")
            if not api_key:
                st.error("Missing Mistral API key!")
                return
                
            if not st.session_state.analysis_result:
                analyzer = AutomataAnalyzer(api_key)
                
                with st.status("Analyzing automata...", expanded=True) as status:
                    try:
                        st.write("Encoding image...")
                        base64_image = analyzer.encode_image(st.session_state.uploaded_file)
                        
                        st.write("Processing with AI...")
                        st.session_state.analysis_result = analyzer.analyze(base64_image)
                        st.session_state.edited_result = st.session_state.analysis_result
                        
                        status.update(label="Analysis complete!", state="complete")
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")
                        status.update(state="error")
                        st.session_state.analysis_result = None
            
            if st.session_state.analysis_result:
                st.subheader("Automata Analysis Results")
                st.warning("⚠️ AI analysis may contain errors. Please review and correct the results before proceeding.")
                
                # Editable text area with improved layout
                with st.container(border=True):
                    edited = st.text_area(
                        "Edit Analysis Results", 
                        value=st.session_state.edited_result,
                        height=400,
                        key="results_editor",
                        label_visibility="collapsed"
                    )
                    
                    # Save button with visual feedback
                    if st.button("💾 Save Edits", use_container_width=True):
                        st.session_state.edited_result = edited
                        st.toast("Edits saved successfully!", icon="✅")

        # Navigation controls
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("← Previous", use_container_width=True):
                st.session_state.current_step = 0
                st.session_state.analysis_result = None
                st.session_state.edited_result = None
                st.rerun()
        with col2:
            if st.button("Next →", 
                       use_container_width=True,
                       disabled=not st.session_state.edited_result):
                st.session_state.current_step = 2
                st.rerun()

    # Step 2: Conversion and Visualization
    elif st.session_state.current_step == 2:
        st.subheader("Step 3: NFA to DFA Conversion")
        
        # Show NFA description
        if st.session_state.edited_result:
            st.subheader("NFA Description")
            st.code(st.session_state.edited_result)
        
        if st.button("Convert to DFA", use_container_width=True):
            try:
                with st.status("Converting NFA to DFA...") as status:
                    # Run conversion pipeline
                    from src.python.converter import convert_to_dfa
                    conversion_log, png_data = convert_to_dfa(st.session_state.edited_result)
                    
                    # Display conversion log
                    st.subheader("Conversion Log")
                    st.code(conversion_log)
                
                col1, col2 = st.columns([1,1])
                with col1:
                    # Show the original NFA diagram
                    st.subheader("Original NFA")
                    if st.session_state.uploaded_file:
                        st.image(st.session_state.uploaded_file, caption="Original State Diagram", use_container_width=True)
                with col2:
                    # Show DFA visualization if available
                    if png_data is not None:
                        st.subheader("DFA Visualization")
                        st.image(png_data, caption="DFA Visualization", use_container_width=True)
                
                # Add download buttons for both diagrams
                col1, col2 = st.columns(2)
                with col1:
                    if st.session_state.uploaded_file:
                        st.download_button(
                            "Download NFA Diagram",
                            st.session_state.uploaded_file,
                            file_name="nfa_diagram.png",
                            mime="image/png"
                        )
                
                with col2:
                    if png_data is not None:
                        st.download_button(
                            "Download DFA Diagram",
                            png_data,
                            file_name="dfa_diagram.png",
                            mime="image/png"
                        )

            except Exception as e:
                st.error(f"Conversion failed: {str(e)}")
        
        # Navigation controls
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("← Previous", use_container_width=True):
                st.session_state.current_step = 1
                st.rerun()
        with col2:
            if st.button("Start again ↻", type="primary", use_container_width=True):
                st.session_state.current_step = 0
                st.rerun()

if __name__ == "__main__":
    main()
