class WorkflowManager:
    def __init__(self, config):
        self.agents = self.initialize_agents(config)
        self.code_execution_approved_by = {"Julia": False, "Mark": False}
        self.messages = []
        self.current_agent = "Florian"

    def initialize_agents(self, config):
        agents = {}
        for agent_name, agent_info in config.items():
            agents[agent_name] = Agent(
                agent_name,
                agent_info["system_message"],
                agent_info["model"],
                agent_info["api_base"],
                agent_info["context_window"],
                agent_info["max_tokens"],
                agent_info["offline"]
            )
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
            return random.choice([name for name in self.agents.keys() if name != "Florian"])
        for name in self.agents.keys():
            if name.lower() in message.lower():
                return name
        return "Florian"

    def process_message(self):
        self.current_agent = self.choose_recipient(self.current_agent, self.messages[-1]["content"])
        agent = self.agents[self.current_agent]
        print(f"Florian(agent): Sending the following prompt to {self.current_agent}:\n{self.messages[-1]['content']}")
        self.messages = agent.chat(self.messages)
        self.messages = self.swap_roles(self.messages)

        # Check for code execution
        if self.messages and "```" in self.messages[-1]["content"]:
            if all(self.code_execution_approved_by.values()):
                print(f"{self.current_agent} (executing code): {self.messages[-1]['content']}")
            else:
                print(f"{self.current_agent} (code execution disabled): {self.messages[-1]['content']}")
        else:
            if self.messages:
                print(f"{self.current_agent}: {self.messages[-1]['content']}")

        # Update approval statuses
        if self.current_agent == "Julia" and self.messages and "approve" in self.messages[-1]["content"].lower():
            self.code_execution_approved_by["Julia"] = True
        if self.current_agent == "Mark" and self.messages and "approve" in self.messages[-1]["content"].lower():
            self.code_execution_approved_by["Mark"] = True

    def start_workflow(self, user_input):
        self.messages.append({"role": "assistant", "type": "message", "content": f"Florian, {user_input}"})
        self.current_agent = "Florian"
        
        while True:
            self.process_message()
            if self.current_agent == "Florian":
                # Check if both Julia and Mark have given their feedback
                if self.code_execution_approved_by["Julia"] and self.code_execution_approved_by["Mark"]:
                    user_satisfied = input("Are you satisfied with the result? (yes/no): ").strip().lower()
                    if user_satisfied == 'yes':
                        print("Workflow completed successfully.")
                        break
                    else:
                        user_input = input("Please provide your new input: ")
                        self.messages = [{"role": "assistant", "type": "message", "content": f"Florian, {user_input}"}]
                        self.current_agent = "Florian"
                        self.code_execution_approved_by = {"Julia": False, "Mark": False}
                else:
                    if not self.code_execution_approved_by["Julia"]:
                        print("Florian(agent): Sending prompt to Julia for code review.")
                        self.messages.append({"role": "assistant", "type": "message", "content": "Julia, can you review the code?"})
                    if not self.code_execution_approved_by["Mark"]:
                        print("Florian(agent): Sending prompt to Mark for security review.")
                        self.messages.append({"role": "assistant", "type": "message", "content": "Mark, can you review the code?"})
            else:
                print(f"Florian(user): Received response from {self.current_agent}.")
