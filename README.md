# Self-Extending Tool System

## Description

This project implements a "Self-Extending Tool System" powered by agents. It allows users to interact with an AI agent that can not only utilize a predefined set of tools but also dynamically create, register, and test new tools based on user requests. This system leverages specialized agents for coordinating tasks, building tools, and validating their functionality.

## Features

* **Agent-Based Interaction:** Uses agents (specifically a Triage Agent) to handle user requests.
* **Tool Utilization:** Can use available tools to fulfill user tasks.
* **Dynamic Tool Creation:** Allows users to request the creation of new tools. A dedicated Tool Builder agent handles the design and implementation.
* **Tool Management:** Includes a registry for storing and managing tool metadata and code. Generated tool code is stored separately.
* **Automated Tool Testing:** A Tool Tester agent validates newly created tools.
* **Extensible Architecture:** Designed with specialized agents that can hand off tasks to each other.

## Architecture

The system consists of several key components:

1.  **Main Entry Point (`main.py`):** Initializes the system, loads environment variables, and runs the main interaction loop, passing user input to the Triage Agent[cite: 1].
2.  **Agents (`dev_agents/`):**
    * **Triage Agent (`triage_agent.py`):** The central coordinator. It interprets user requests, uses existing tools, or delegates tasks (like tool creation) to other specialized agents.
    * **Tool Builder Agent (`tool_builder.py`):** Responsible for creating new tools based on specifications. It checks for existing tools, designs the new tool, writes the code, registers it, and hands off to the Tool Tester.
    * **Tool Tester Agent (`tool_tester.py`):** Validates newly created tools by designing and running test cases.
3.  **Tool Management (`tools/`):**
    * **Management (`management.py`):** Provides the core functions (`get_tools`, `use_tool`, `create_tool`) that agents use to interact with the tool system.
    * **Registry (`registry.py`):** Manages the persistence of tools. It loads/saves tool metadata to `tool_registry.json` and stores the generated Python code for each tool in the `tools/generated/` directory.
    * **Generated Tools (`tools/generated/`):** Contains the Python files for each tool (e.g., `simple_calculator.py`, `fibonacci_calculator.py`).

## Getting Started

### Prerequisites

* Python 3.x

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd self_extending_agent
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    This will install packages like `openai-agents`, `python-dotenv`, and `pydantic`.

### Configuration

* The system uses `python-dotenv` to load environment variables from a `.env` file in the project root[cite: 1]. Create a `.env` file with your OPENAI_API_KEY. 

### Running the Application

* Execute the main script from the project's root directory:
    ```bash
    python main.py
    ```
    This will start the interactive command-line interface.

## Usage

Once the application is running, you can interact with it by typing requests into the console when prompted. Examples include:

* **Listing available tools:** "What tools are available?"
* **Using an existing tool:** "Use the simple_calculator to add 5 and 3"
* **Requesting a new tool:** "I need a tool that converts Celsius to Fahrenheit"

To exit the application, type `exit` and press Enter[cite: 1]. The Triage Agent will process your request, potentially using existing tools or initiating the tool creation and testing workflow involving the Tool Builder and Tool Tester agents.
