import random
from interpreter import OpenInterpreter

class Agent:
    def __init__(self, name, system_message, model, api_base, context_window=3000, max_tokens=512, offline=True):
        self.name = name
        self.interpreter = OpenInterpreter()
        self.interpreter.system_message = system_message
        self.interpreter.llm.model = model
        self.interpreter.llm.api_base = api_base
        self.interpreter.context_window = context_window
        self.interpreter.max_tokens = max_tokens
        self.interpreter.offline = offline
        self.allow_code_execution = False
    
    def chat(self, messages):
        return self.interpreter.chat(messages)

class WorkflowManager:
    def __init__(self):
        self.agents = self.initialize_agents()
        self.code_execution_approved_by = {"Julia": False, "Mark": False}
        self.messages = [{"role": "user", "type": "message", "content": "Hello, my name is Wolfgang. I'm an inexperienced noob who should run an IT system without any documentation. I need your help."}]
        self.current_agent = "Florian"

    def initialize_agents(self):
        agents = {
            "Hans-Peter": Agent("Hans-Peter", "Hans-Peter, you are an experienced System Administrator with great knowledge on all IT-related topics.", "ollama_chat/command-r", "http://localhost:11434"),
            "Monica": Agent("Monica", "Monica, you are a System Administrator specialized in analyzing code and logs. You are a great help for Hans-Peter.", "ollama_chat/starcoder", "http://localhost:11434"),
            "Martin": Agent("Martin", "Martin, you are a skilled Python Programmer. Your code is object-oriented and follows the MVC model. You send your generated code for analyzing to Julia.", "ollama_chat/starcoder", "http://localhost:11434"),
            "Julia": Agent("Julia", "Julia, you have a deep understanding of code analysis and debugging. You work closely with Martin. If he sends code to you, analyze it and provide feedback.", "ollama_chat/codegemma", "http://localhost:11434"),
            "Brigitte": Agent("Brigitte", "Brigitte, you are a technical writer who knows that a clean presentation of information is crucial for understandability, has full knowledge about markdown, and knows everything about the BookStack wiki system. You are also very good at structuring and organizing information.", "ollama_chat/command-r", "http://localhost:11434"),
            "Mark": Agent("Mark", "Mark, you are a security expert with deep knowledge of IT security protocols, threat detection, and system hardening. You review system configurations and code to ensure they meet security standards.", "ollama_chat/codegemma", "http://localhost:11434"),
            "Florian": Agent("Florian", "Florian, you are a team leader with a strong understanding of natural language processing and excellent coordination skills. Your role is to manage the team, understand the requirements, and write effective prompts for the team members to ensure optimal results.", "ollama_chat/command-r", "http://localhost:11434")
        }
        return agents

    def swap_roles(self, messages):
        for message in messages:
            if message['role'] == 'user':
                message['role'] = 'assistant'
            elif message['role'] == 'assistant':
                message['role'] = 'user'
        return messages

    def choose_recipient(self, agent_name, message):
        if agent_name == "Florian":
            return random.choice(["Hans-Peter", "Monica", "Martin", "Julia", "Brigitte", "Mark"])
        for name in self.agents.keys():
            if name.lower() in message.lower():
                return name
        return "Florian"

    def process_message(self):
        self.current_agent = self.choose_recipient(self.current_agent, self.messages[-1]["content"])
        agent = self.agents[self.current_agent]
        self.messages = agent.chat(self.messages)
        self.messages = self.swap_roles(self.messages)

        # Check for code execution
        if "```" in self.messages[-1]["content"]:
            if all(self.code_execution_approved_by.values()):
                print(f"{self.current_agent} (executing code): {self.messages[-1]['content']}")
            else:
                print(f"{self.current_agent} (code execution disabled): {self.messages[-1]['content']}")
        else:
            print(f"{self.current_agent}: {self.messages[-1]['content']}")

        # Update approval statuses
        if self.current_agent == "Julia" and "approve" in self.messages[-1]["content"].lower():
            self.code_execution_approved_by["Julia"] = True
        if self.current_agent == "Mark" and "approve" in self.messages[-1]["content"].lower():
            self.code_execution_approved_by["Mark"] = True

    def run(self):
        while True:
            self.process_message()

# Run the workflow
workflow_manager = WorkflowManager()
workflow_manager.run()
