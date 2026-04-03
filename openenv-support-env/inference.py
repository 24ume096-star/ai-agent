import os
import json
import asyncio
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://openrouter.ai/api/v1")
API_KEY = os.getenv("OPENAI_API_KEY", "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")
MODEL_NAME = os.getenv("MODEL_NAME", "stepfun/step-3.5-flash:free")

def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step, action, reward, done, error):
    err_str = f" error={error}" if error else ""
    print(f"[STEP] step={step} action={action} reward={reward} done={done}{err_str}", flush=True)

def log_end(success, steps, score, rewards):
    print(f"[END] success={success} steps={steps} score={score}", flush=True)

async def main():
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY,
        default_headers={
            "HTTP-Referer": "https://github.com/openenv",
            "X-Title": "OpenEnv"
        }
    )

    from app.env import SupportEnv
    from app.models import Action
    from app.graders import grade_task
    
    env = SupportEnv()
    tasks_to_run = ["easy", "medium", "hard"]
    leaderboard = {}

    for task_difficulty in tasks_to_run:
        log_start(f"support-task-{task_difficulty}", "support-env", MODEL_NAME)

        obs = env.reset(task_difficulty)
        rewards = []
        
        system_prompt = """You are an AI customer support agent. Follow this strategy strictly:
1. First, search the knowledge base using the 'search' action to find relevant policy information based on the customer's issue.
2. Read the search results carefully to formulate an accurate and policy-compliant response.
3. Then, reply to the customer using the 'reply' action with the accurate information.
4. If a ticket is complex and explicitly requires escalation, use the 'escalate' action. Do NOT escalate easy or standard tickets.
You must use the provided tools to take exactly one action per step."""
        
        tools = [{
            "type": "function",
            "function": {
                "name": "take_action",
                "description": "Takes an action in the support environment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action_type": {
                            "type": "string", 
                            "enum": ["classify", "search", "reply", "escalate"]
                        },
                        "content": {
                            "type": "string", 
                            "description": "Content of action (keywords to search, reply message, or classification label)."
                        }
                    },
                    "required": ["action_type", "content"]
                }
            }
        }]

        messages = [
            {"role": "system", "content": system_prompt}
        ]

        for step in range(5):
            await asyncio.sleep(2) # Prevent Free-Tier Rate Limits
            obs_json = obs.model_dump_json() if hasattr(obs, "model_dump_json") else obs.json()
            messages.append({"role": "user", "content": f"Observation:\n{obs_json}"})
            
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    tools=tools
                )
                
                if response.choices[0].message.tool_calls:
                    tool_call = response.choices[0].message.tool_calls[0]
                    action_data = json.loads(tool_call.function.arguments)
                    action_type = action_data.get("action_type", "classify")
                    content_val = action_data.get("content", "refund")
                else:
                    content_str = response.choices[0].message.content or "{}"
                    if "```json" in content_str:
                        content_str = content_str.split("```json")[1].split("```")[0]
                    elif "```" in content_str:
                        content_str = content_str.split("```")[1].split("```")[0]
                        
                    action_data = json.loads(content_str.strip())
                    action_type = action_data.get("action_type", "classify")
                    content_val = action_data.get("content", "refund")
                    
                content = content_val if isinstance(content_val, str) else json.dumps(content_val)
            except Exception as e:
                print(f"  Error parsing LLM response: {e}")
                action_type = "classify"
                content = "refund"

            action_text = f"{action_type}: {content}"
            messages.append({"role": "assistant", "content": f"Action taken: {action_text}"})

            result = env.step(
                Action(
                    action_type=action_type,
                    content=content
                )
            )

            obs = result["observation"]
            rewards.append(result["reward"])

            log_step(step, action_text, result["reward"], result["done"], None)

            if action_type == "reply" and not result["done"]:
                print("  [SYSTEM] Simulated Customer is replying...")
                sim_res = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are a customer. The agent just gave an unhelpful/incorrect response. Reply briefly with frustration."},
                        {"role": "user", "content": f"Agent said: {content}. Your original issue: {env.state_data['message']}"}
                    ]
                )
                sim_msg = sim_res.choices[0].message.content.strip()
                env.add_customer_message(sim_msg)
                obs = env._get_observation()
                print(f"  [CUSTOMER] {sim_msg}")

            if result["done"]:
                break

        final_score = grade_task(env.state())
        leaderboard[task_difficulty] = final_score
        log_end(True, step + 1, final_score, rewards)

    print("\n=== FINAL LEADERBOARD ===")
    print(f"Model ID: {MODEL_NAME}")
    for diff, score in leaderboard.items():
        print(f"{diff.capitalize()} Ticket Score: {score}")

if __name__ == "__main__":
    asyncio.run(main())