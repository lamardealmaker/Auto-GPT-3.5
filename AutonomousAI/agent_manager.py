import openai

next_key = 0
agents = {} # key, (task, full_message_history)

# Create new GPT agent
def create_agent(task, prompt, model):
    global next_key
    global agents

    messages = [{"role": "user", "content": prompt},]

    # Start GTP3 instance
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )

    agent_reply = response.choices[0].message["content"]

    # Update full message history
    messages.append({"role": "assistant", "content": agent_reply})

    key = next_key
    next_key += 1 # This is done instead of len(agents) to make keys unique even if agents are deleted

    agents[key] = (task, messages)

    return key, agent_reply

def message_agent(key, message):
    global agents

    task, messages = agents[key]

    # Add user message to message history before sending to agent
    messages.append({"role": "user", "content": message})

    # Start GTP3 instance
    response = openai.ChatCompletion.create(
        model="model",
        messages=messages,
    )

    # Get agent response
    agent_reply = response.choices[0].message["content"]

    # Update full message history
    messages.append({"role": "assistant", "content": agent_reply})

    return agent_reply

def list_agents():
    global agents

    # Return a list of agent keys and their tasks
    return [(key, task) for key, (task, _) in agents.items()]

def delete_agent(key):
    global agents

    try:
        del agents[key]
        return True
    except KeyError:
        return False


