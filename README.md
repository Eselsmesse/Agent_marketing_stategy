
# AI Crew for Marketing Strategy
## Introduction
This project demonstrates the use of the CrewAI framework to automate the creation of a marketing strategy. CrewAI orchestrates autonomous AI agents, enabling them to collaborate and execute complex tasks efficiently using DeepSeek LLM.

By [@joaomdmoura](https://x.com/joaomdmoura)

- [CrewAI Framework](#crewai-framework)
- [DeepSeek LLM Integration](#deepseek-llm-integration)
- [Running the script](#running-the-script)
- [Details & Explanation](#details--explanation)
- [Contributing](#contributing)
- [Support and Contact](#support-and-contact)
- [License](#license)

## CrewAI Framework
CrewAI is designed to facilitate the collaboration of role-playing AI agents. In this example, these agents work together to create a comprehensive marketing strategy and develop compelling marketing content.

## DeepSeek LLM Integration
This project uses DeepSeek LLM for all AI operations:

### DeepSeek Models
- **deepseek-chat** - DeepSeek Chat (основная модель)
- **deepseek-coder** - DeepSeek Coder (для технических задач)

## Running the Script
The project uses DeepSeek LLM by default for all AI operations.

- **Configure Environment**: Copy `env_example.txt` to `.env` and set up the environment variables:
  - [DeepSeek](https://platform.deepseek.com/) for DeepSeek models
  - [Serper](serper.dev) for web search functionality
- **Install Dependencies**: Run `uv sync` to install dependencies.
- **Customize**: Modify `src/marketing_posts/main.py` to add custom inputs for your agents and tasks.
- **Customize Further**: Check `src/marketing_posts/config/agents.yaml` to update your agents and `src/marketing_posts/config/tasks.yaml` to update your tasks.
- **Execute the Script**: Run with DeepSeek LLM:

### Usage Examples

```bash
# Использование DeepSeek (по умолчанию)
uv run marketing_posts

# Использование конкретной модели DeepSeek
uv run marketing_posts --model deepseek-chat

# Использование DeepSeek Coder
uv run marketing_posts --model deepseek-coder

# Обучение с DeepSeek
uv run marketing_posts --train 5

# Обучение с конкретной моделью
uv run marketing_posts --model deepseek-coder --train 3
```

## Details & Explanation
- **Running the Script**: Execute `uv run marketing_posts` with appropriate arguments. The script will leverage the CrewAI framework with DeepSeek LLM to generate a detailed marketing strategy.
- **Key Components**:
  - `src/marketing_posts/main.py`: Main script file with DeepSeek LLM integration.
  - `src/marketing_posts/crew.py`: Main crew file where agents and tasks come together, and the main logic is executed.
  - `src/marketing_posts/config/llm_config.py`: DeepSeek LLM configuration.
  - `src/marketing_posts/config/agents.yaml`: Configuration file for defining agents.
  - `src/marketing_posts/config/tasks.yaml`: Configuration file for defining tasks.
  - `src/marketing_posts/tools`: Contains tool classes used by the agents.

## License
This project is released under the MIT License.
