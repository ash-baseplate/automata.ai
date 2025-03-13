# Automata.ai

A web application for converting Non-deterministic Finite Automata (NFA) to Deterministic Finite Automata (DFA) with AI-powered diagram analysis.

## Features

- **AI-powered Diagram Analysis**: Upload images of NFA diagrams and have them automatically analyzed
- **Interactive Editing**: Review and edit the AI analysis results before conversion
- **NFA to DFA Conversion**: Convert NFAs to DFAs using the subset construction algorithm
- **Visualization**: View and download both the original NFA and the converted DFA diagrams

## Architecture

The application consists of:

1. **Frontend**: Streamlit-based web interface
2. **AI Analysis**: Mistral AI vision model for analyzing automata diagrams
3. **Conversion Engine**: C++ implementation of the subset construction algorithm
4. **Visualization**: Graphviz-based rendering of the resulting DFA

## Installation

### Prerequisites

- Python 3.8+
- C++ compiler (g++ with C++17 support)
- Graphviz

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/automata-converter.git
   cd automata-converter
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Mistral API key:
   - Create a `.streamlit/secrets.toml` file with:
     ```toml
     MISTRAL_API_KEY = "your-mistral-api-key"
     ```

## Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Follow the steps in the application:
   - Upload an image of an NFA diagram
   - Review and edit the AI analysis results
   - Convert the NFA to a DFA
   - View and download the visualizations

## Development

### Project Structure
automata-converter/
├── app.py # Main Streamlit application
├── src/
│ ├── python/
│ │ ├── ai.py # AI-powered diagram analyzer
│ │ ├── converter.py # Python interface to C++ converter
│ │ └── visualizer.py # DFA visualization module
│ └── cpp/
│ └── converter.cpp # C++ implementation of NFA to DFA conversion
├── requirements.txt # Python dependencies
└── .streamlit/
└── secrets.toml # API keys (not in repository)

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Mistral AI for providing the vision model capabilities
- Graphviz for graph visualization
- Streamlit for the web application framework
