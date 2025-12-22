from huggingface_hub import InferenceClient
import traceback

# 1. SETUP
# Replace with your actual token
TOKEN = "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"

print("--- Starting AI Connection Test ---")

try:
    # Initialize Client
    client = InferenceClient(token=TOKEN)
    
    # 2. TEST 1: Simple Connection (GPT2 is small and reliable)
    print("Test 1: Pinging GPT-2 (Connection Check)...")
    response = client.text_generation(
        model="gpt2", 
        prompt="The sky is blue because", 
        max_new_tokens=10
    )
    print("✅ Test 1 Success! Response:", response)

    # 3. TEST 2: Your Actual Model (Flan-T5)
    print("\nTest 2: Pinging Flan-T5 (Your Model)...")
    response_t5 = client.text_generation(
        model="google/flan-t5-large", 
        prompt="Explain quantum physics.", 
        max_new_tokens=10
    )
    print("✅ Test 2 Success! Response:", response_t5)

except Exception:
    # This prints the FULL error details, not just the short message
    print("\n❌ ERROR DETECTED:")
    traceback.print_exc()