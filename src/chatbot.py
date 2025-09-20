from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

# Initialize the model and tokenizer
model_name = "facebook/blenderbot-400M-distill"
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

def chat_with_bot(input_text):
    """
    Takes user input as text, generates a response using the chatbot model, and returns the response.
    """
    inputs = tokenizer(input_text, return_tensors="pt")
    response_ids = model.generate(
        **inputs,
        max_length=100,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        do_sample=True
    )
    return tokenizer.decode(response_ids[0], skip_special_tokens=True)

if __name__ == "__main__":
    import sys
    try:
        input_text = sys.stdin.read().strip()
        if not input_text:
            raise ValueError("No input received.")
        response = chat_with_bot(input_text)
        print(response)
    except Exception as e:
        print(f"Error: {str(e)}")
