import urllib.request
import json
import ssl
import sys
import os

# 全面模型映射表
MODEL_MAP = {
    # --- 国产大模型 ---
    "glm5": "z-ai/glm5",
    "glm4": "z-ai/glm4.7",
    "kimi": "moonshotai/kimi-k2.5",
    "kimi-think": "moonshotai/kimi-k2-thinking",
    "minimax": "minimaxai/minimax-m2.1",
    "yi": "01-ai/yi-large",
    "qwen": "qwen/qwen2.5-7b-instruct",
    "qwq": "qwen/qwq-32b",
    "deepseek": "deepseek-ai/deepseek-v3.1",
    "r1-llama-8b": "deepseek-ai/deepseek-r1-distill-llama-8b",
    "r1-qwen-32b": "deepseek-ai/deepseek-r1-distill-qwen-32b",

    # --- 国际顶尖模型 ---
    "llama4": "meta/llama-4-scout-17b-16e-instruct",
    "llama33": "meta/llama-3.3-70b-instruct",
    "llama31-405b": "meta/llama-3.1-405b-instruct",
    "llama31-70b": "meta/llama-3.1-70b-instruct",
    "llama-vision": "meta/llama-3.2-90b-vision-instruct",
    "mistral-large": "mistralai/mistral-large-3-675b-instruct-2512",
    "mixtral": "mistralai/mixtral-8x22b-instruct-v0.1",
    "gemma3": "google/gemma-3-27b-it",
    "phi4": "microsoft/phi-4-mini-instruct",
    "phi35-moe": "microsoft/phi-3.5-moe-instruct",

    # --- NVIDIA 优化模型 ---
    "nemotron": "nvidia/llama-3.1-nemotron-70b-instruct",
    "nemotron-mini": "nvidia/nemotron-mini-4b-instruct",
}

def call_nim(model_alias, prompt):
    model_id = MODEL_MAP.get(model_alias.lower(), model_alias)
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        return "Error: NVIDIA_API_KEY not found in environment."
        
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2048
    }
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
        with urllib.request.urlopen(req, context=ctx) as response:
            result = json.loads(response.read().decode())
            return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

def list_models():
    print("\n--- 可用模型别名列表 ---")
    print(f"{'别名':<15} | {'NVIDIA 模型 ID'}")
    print("-" * 50)
    for alias, mid in sorted(MODEL_MAP.items()):
        print(f"{alias:<15} | {mid}")
    print("-" * 50)
    print("提示: 你也可以直接使用未列出的完整模型 ID。\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 nim_call.py <alias|list> [prompt]")
    elif sys.argv[1].lower() == "list":
        list_models()
    elif len(sys.argv) >= 3:
        alias = sys.argv[1]
        task = " ".join(sys.argv[2:])
        print(call_nim(alias, task))
    else:
        print("错误: 缺少任务内容。如果是查看模型列表，请用 'list'。")
