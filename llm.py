



import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import dataHandler


model_name = "Qwen/Qwen3-1.7B"
# load the tokenizer and the model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)



def main(chat, chatId):

    

    # prepare the model input
    
    messages = chat
    print("messages:", messages)
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=True # Switches between thinking and non-thinking modes. Default is True.
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    print("conditioning text complete, start generating...")
    # conduct text completion
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=32768
    )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

    print("parsing output...")
    # parsing thinking content
    try:
        # rindex finding 151668 (</think>)
        index = len(output_ids) - output_ids[::-1].index(151668)
    except ValueError:
        index = 0

    thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
    dataHandler.appendToChat(chatId, "assistant", thinking_content)
    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")
    dataHandler.appendToChat(chatId, "assistant", content)


    print("thinking content:", thinking_content)
    print("content:", content)



if __name__ == "__main__":
    print("start testing...")
    prompt = "Give me a short introduction to large language model."
    main([{"role": "user", "content": prompt}], "0x902d9d2b")