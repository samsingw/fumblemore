class Agent:
    def __init__(self, name, system_message, model, api_base, context_window=3000, max_tokens=512, offline=True):
        self.name = name
        self.system_message = system_message
        self.model = model
        self.api_base = api_base
        self.context_window = context_window
        self.max_tokens = max_tokens
        self.offline = offline
        self.interpreter = OpenInterpreter()
        self.setup_interpreter()

    def setup_interpreter(self):
        self.interpreter.system_message = self.system_message
        self.interpreter.llm.model = self.model
        self.interpreter.llm.api_base = self.api_base
        self.interpreter.context_window = self.context_window
        self.interpreter.max_tokens = self.max_tokens
        self.interpreter.offline = self.offline

    def chat(self, messages):
        return self.interpreter.chat(messages)
