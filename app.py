from fastapi import FastAPI, HTTPException
import razorpay

app = FastAPI()

# Initialize Razorpay client with your API keys
razorpay_client = razorpay.Client(auth=("rzp_test_N97KSHc0rITx3P", "IRl8oZFZwOhPPhMJ5BJeRPIx"))

@app.post("/create-payment")
async def create_payment(amount: int):
    # Create a Razorpay payment order
    payment_data = {
        "amount": amount * 200,  # Convert amount to paisa (currency's smallest unit)
        "currency": "INR",
        "receipt": "order_receipt_1",
        "payment_capture": 1
    }

    try:
        payment = razorpay_client.order.create(data=payment_data)
        return {"order_id": payment["id"]}
    except Exception as e:
        return {"error": str(e)}

@app.get("/verify-payment/{order_id}")
async def verify_payment(order_id: str):
    try:
        # Fetch the payment details from Razorpay using the order ID
        order = razorpay_client.order.fetch(order_id)
        payment_id = order.get("payments")[0]["payment_id"]
        
        # Fetch the payment details using the payment ID
        payment = razorpay_client.payment.fetch(payment_id)
        
        # Check the payment status
        status = payment.get("status")
        return {"payment_status": status}
    except Exception as e:
        return {"error": str(e)}
