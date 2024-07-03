import json

def load_config(config_path):
    with open(config_path, "r") as file:
        return json.load(file)

if __name__ == "__main__":
    config_path = "config.json"
    config = load_config(config_path)
    workflow_manager = WorkflowManager(config)
    user_input = input("Please enter your initial task: ")
    workflow_manager.start_workflow(user_input)
