# 🤖 Kimi API

> A simple yet working Python client for interacting with the Kimi AI assistant

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-kimi4free-orange.svg)](https://pypi.org/project/kimi4free/)

## 🚀 Installation

```bash
pip install kimi4free
```

## ⚡ Quick Start

```python
from kimi4free import KimiClient

# Initialize the client
client = KimiClient()

# 💬 Get response without streaming
response = client.chat("Hello, how are you?")
print(response)

# 🌊 Stream response to console
response = client.chat("Tell me a joke", stream=True)
print(f"\nComplete response: {response}")
```

## 📖 Usage

### 💭 Basic Chat

```python
from kimi4free import KimiClient

# Create client instance
client = KimiClient()

# Simple chat interaction
response = client.chat("What's 2+2?")
print(response)
```

### 🌊 Streaming Response

```python
# Stream output to console while building full response
response = client.chat("Write a short poem", stream=True)
print(f"\n\nFull poem: {response}")
```

### ⚙️ Advanced Parameters

```python
# 🔍 Disable search and deep research
response = client.chat(
    "Hello", 
    use_search=False, 
    use_deep_research=False
)

# 🎯 Use different model
response = client.chat("Hi there", model="k2")
```

## 📚 API Reference

### 🏗️ `KimiClient()`

Creates a new Kimi API client instance.

### 💬 `client.chat(message, **kwargs)`

Send a message and create a new chat session.

**Parameters:**
- 📝 `message` (str): Your message
- 🌊 `stream` (bool): Stream output to console (default: `False`)
- 🤖 `model` (str): AI model to use (default: `"k2"`)
- 🔍 `use_search` (bool): Enable web search (default: `True`)
- 🔬 `use_deep_research` (bool): Enable deep research (default: `True`)
- 🧠 `use_semantic_memory` (bool): Use semantic memory (default: `False`)

**Returns:** 📤 Complete response text

### 🆕 `client.create_chat()`

Create a new chat session.

**Returns:** 🆔 Chat ID string

### 📨 `client.send_message(chat_id, message, **kwargs)`

Send a message to an existing chat session.

**Parameters:**
- 🆔 `chat_id` (str): Chat session ID
- 📝 `message` (str): Your message
- ⚙️ All parameters from `chat()` method

**Returns:** 📤 Complete response text

## 🎯 Features

- 🌊 Real-time streaming support
- 🔍 Web search integration
- 🔬 Deep research capabilities
- 📱 Lightweight and fast

## 🤝 Contributing

We welcome contributions! We are still missing upload functionnality, feel free to pull request !

## 📄 License

This project is licensed under the MIT License.

## 💖 Support

If you find this project helpful:

- ⭐ Star this repository
- 🐛 Report issues
- 💡 Suggest new features
- 🤝 Contribute code

---

<div align="center">

**Made with ❤️ by the community**

[⭐ Star on GitHub](https://github.com/SertraFurr/kimi4free) • [📦 PyPI Package](https://pypi.org/project/kimi4free/)

</div>
