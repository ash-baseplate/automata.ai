"""
NFA to DFA converter module.

This module provides functionality to convert an NFA description to a DFA
by interfacing with the C++ implementation and handling the conversion process.
"""

import os
import subprocess
import tempfile
from .visualizer import visualize_dfa

def parse_nfa_description(description):
    """
    Convert user-friendly format to C++ program input format.
    
    Args:
        description (str): NFA description in user-friendly format
        
    Returns:
        str: Formatted input for the C++ program
        
    Raises:
        ValueError: If parsing fails
    """
    lines = description.strip().split('\n')
    data = {}
    transitions = []
    
    # print("Parsing NFA description:")
    # print(description)
    
    i = 0
    try:
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
                
            if "Enter number of states:" in line:
                num_states = lines[i].split(':')[1].strip()
                states = lines[i + 1].split(':')[1].strip()
                i += 2
                
            elif "Enter number of symbols:" in line:
                num_symbols = lines[i].split(':')[1].strip()
                symbols = lines[i + 1].split(':')[1].strip()
                i += 2
                
            elif "Enter start state:" in line:
                start_state = lines[i].split(':')[1].strip()
                i += 1
                
            elif "Enter number of accepting states:" in line:
                num_accepting = lines[i].split(':')[1].strip()
                accepting_states = lines[i + 1].split(':')[1].strip()
                i += 2
                
            elif "Enter number of transitions:" in line:
                num_transitions = int(lines[i].split(':')[1].strip())
                i += 1
                # Collect all transitions
                for _ in range(num_transitions):
                    if i < len(lines) and "Enter transition" in lines[i]:
                        trans = lines[i].split(':')[1].strip()
                        if trans:  # Only add non-empty transitions
                            transitions.append(trans)
                    i += 1
            else:
                i += 1
    
        # Create the compact format
        cpp_input = [
            num_states,
            states,
            num_symbols,
            symbols,
            start_state,
            num_accepting,
            accepting_states,
            str(len(transitions))
        ]
        cpp_input.extend(transitions)
        
        result = "\n".join(cpp_input)
        # print("\nParsed C++ input:")
        # print(result)
        return result
        
    except Exception as e:
        raise ValueError(f"Error preparing NFA data: {str(e)}")

def convert_to_dfa(nfa_description):
    """
    Converts NFA to DFA using the C++ program.
    
    Args:
        nfa_description (str): Description of the NFA
        
    Returns:
        tuple: (conversion_output, png_data) where conversion_output is the text output
               from the C++ program and png_data is the visualization of the DFA
               
    Raises:
        Exception: If conversion fails
    """
    try:
        # Parse the user-friendly format to C++ input format
        cpp_input = parse_nfa_description(nfa_description)
        
        # Get the absolute path to the cpp file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cpp_file = os.path.join(current_dir, "..", "cpp", "converter.cpp")
        
        with tempfile.NamedTemporaryFile(suffix='.exe', delete=False) as temp_exe:
            exe_path = temp_exe.name
            
        try:
            # Compile the C++ program to temporary executable
            compile_command = f"g++ {cpp_file} -o {exe_path} -std=c++17"
            subprocess.run(compile_command, shell=True, check=True, capture_output=True)
            
            # Run the converter with parsed input
            result = subprocess.run(
                [exe_path],
                input=cpp_input,
                text=True,
                capture_output=True,
                check=True
            )
            
            # Generate visualization if dot file exists
            if os.path.exists('dfa.dot'):
                png_data = visualize_dfa()
            else:
                png_data = None
            
            return result.stdout, png_data
            
        finally:
            # Clean up temporary executable
            if os.path.exists(exe_path):
                os.unlink(exe_path)
        
    except subprocess.CalledProcessError as e:
        raise Exception(f"Program execution failed: {str(e)}\nStderr: {e.stderr}")
    except FileNotFoundError as e:
        raise Exception(f"File error: {str(e)}")
    except ValueError as e:
        raise Exception(f"Input parsing failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Conversion error: {str(e)}")