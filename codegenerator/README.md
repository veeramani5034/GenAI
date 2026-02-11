# AI Code Generator

A simple AI-powered code generator using OpenAI GPT and Streamlit. Generate code in any programming language with natural language descriptions.

## Features

- 🤖 AI-powered code generation using GPT-4
- 💻 Support for multiple programming languages
- 📝 Code explanation and documentation
- 🔧 Code debugging and optimization
- 📋 Copy to clipboard functionality
- 🎨 Syntax highlighting
- 💾 Download generated code

## Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API Key

### Installation

```bash
# Navigate to project
cd codegenerator

# Install dependencies
pip install streamlit openai python-dotenv

# Create .env file
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-key-here

# Run the app
streamlit run app.py
```

## Usage

1. **Enter your OpenAI API key** (if not set as environment variable)
2. **Select programming language** (Python, JavaScript, Java, etc.)
3. **Choose task type**:
   - Generate new code
   - Explain existing code
   - Debug code
   - Optimize code
   - Add documentation
4. **Describe what you want** in natural language
5. **Click Generate** and get your code!

## Example Prompts

### Generate Code
```
Create a function to calculate fibonacci numbers recursively
```

### Explain Code
```
Explain this code:
def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)
```

### Debug Code
```
Fix this code:
def add(a, b)
    return a + b
```

### Optimize Code
```
Optimize this bubble sort implementation for better performance
```

## Supported Languages

- Python
- JavaScript
- TypeScript
- Java
- C++
- C#
- Go
- Rust
- PHP
- Ruby
- Swift
- Kotlin
- And more!

## Features in Detail

### Code Generation
- Generate functions, classes, algorithms
- Create complete applications
- Build API endpoints
- Design database schemas

### Code Explanation
- Understand complex code
- Learn new concepts
- Get step-by-step breakdowns

### Code Debugging
- Find and fix errors
- Identify edge cases
- Improve error handling

### Code Optimization
- Improve performance
- Reduce complexity
- Follow best practices

## Tips for Best Results

1. **Be specific** - Provide clear requirements
2. **Include context** - Mention frameworks, libraries
3. **Specify constraints** - Performance, memory, etc.
4. **Provide examples** - Input/output samples help
5. **Iterate** - Refine based on results

## Example Use Cases

### Web Development
```
Create a React component for a user profile card with avatar, name, and bio
```

### Data Science
```
Write a Python function to clean and preprocess CSV data
```

### Algorithms
```
Implement a binary search tree with insert, delete, and search methods
```

### API Development
```
Create a REST API endpoint in Express.js for user authentication
```

## Keyboard Shortcuts

- `Ctrl + Enter` - Generate code
- `Ctrl + C` - Copy code
- `Ctrl + S` - Download code

## Troubleshooting

### API Key Issues
- Ensure your OpenAI API key is valid
- Check you have credits: https://platform.openai.com/usage
- Verify no extra spaces in the key

### Generation Errors
- Try simplifying your prompt
- Be more specific about requirements
- Check language selection matches your request

### Slow Response
- GPT-4 can take 10-30 seconds
- Try GPT-3.5-turbo for faster results
- Check your internet connection

## Configuration

You can customize the app by modifying these settings in the sidebar:

- **Model**: GPT-4 (better quality) or GPT-3.5-turbo (faster)
- **Temperature**: 0.0 (deterministic) to 1.0 (creative)
- **Max Tokens**: Control response length

## Privacy & Security

- Your API key is stored only in your browser session
- Code is sent to OpenAI for processing
- No data is stored on our servers
- Use environment variables for production

## Cost Estimation

Approximate costs per request:
- GPT-4: $0.03 - $0.10
- GPT-3.5-turbo: $0.001 - $0.005

Monitor usage: https://platform.openai.com/usage

## Deployment

### Local
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add OpenAI API key in secrets
4. Deploy!

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY app.py .
RUN pip install streamlit openai python-dotenv
CMD ["streamlit", "run", "app.py"]
```

## Contributing

Feel free to enhance this code generator:
- Add more languages
- Improve prompts
- Add code templates
- Enhance UI/UX

## License

MIT License - Free to use and modify!

## Support

For issues or questions:
- Check OpenAI documentation
- Review Streamlit docs
- Open an issue on GitHub

## Acknowledgments

- Built with Streamlit
- Powered by OpenAI GPT
- Inspired by GitHub Copilot

---

**Happy Coding! 🚀**
