"""
DFA visualization module.

This module provides functionality to visualize DFA diagrams
using Graphviz from DOT file representations.
"""

import graphviz
import os

def visualize_dfa(dot_file_path="dfa.dot"):
    """
    Converts the DOT file to PNG visualization.
    
    Args:
        dot_file_path (str): Path to the DOT file
        
    Returns:
        bytes: PNG image data of the visualized DFA
        
    Raises:
        Exception: If visualization fails
    """
    try:
        # Read the DOT file
        with open(dot_file_path, 'r') as f:
            dot_content = f.read()
        
        # Create a Graphviz object
        graph = graphviz.Source(dot_content)
        
        # Render directly to bytes
        return graph.pipe(format='png')
        
    except Exception as e:
        raise Exception(f"Visualization failed: {str(e)}")

# Call the function to visualize the DFA
visualize_dfa()
