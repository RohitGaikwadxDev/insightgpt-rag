from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
import torch


MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"


# Select GPU when CUDA is available.
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


print(f"Using device: {device}")

if torch.cuda.is_available():
    print(
        f"GPU: {torch.cuda.get_device_name(0)}"
    )


tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)


model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16
)

model = model.to(device)

model.eval()


def generate_answer(
    prompt: str,
    max_new_tokens: int = 120
) -> str:

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]


    formatted_prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )


    inputs = tokenizer(
        formatted_prompt,
        return_tensors="pt"
    ).to(device)


    with torch.inference_mode():

        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            repetition_penalty=1.2,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id
        )


    input_length = inputs["input_ids"].shape[1]

    generated_tokens = outputs[0][input_length:]


    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )


    return answer.strip()