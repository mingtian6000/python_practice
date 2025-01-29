from modelscope import AutoModelForCausalLM, AutoTokenizer, snapshot_download
from modelscope import GenerationConfig

def chat1_5(model, tokenizer, ques, history=[], temperature = 0.7):
    if history == []:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": ques}
        ]
    else:
        messages = history
        messages.append({"role": "user", "content": ques})
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt")
    
    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512,
        temperature = temperature
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    messages.append({
        "role": "system", "content": response
    })
    history = messages
    return response, history


##cache_dir表示模型存储的目录 models_dir = r"C:\Users\alice\.cache\modelscope\hub\qwen\"
#models_dir = r"C:/Users/alice/LLMmodels/"
model_dir = snapshot_download('qwen/Qwen2.5-1.5B-Instruct')
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_dir, torch_dtype="auto",device_map="cpu",trust_remote_code=True).eval()

print(model)

model.generation_config = GenerationConfig.from_pretrained(model_dir, trust_remote_code=True)
response, history = chat1_5(model, tokenizer, "你好！可以介绍一下大语言模型吗",history=[])
print(response)
