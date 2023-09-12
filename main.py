from fastapi import FastAPI
import razorpay

app = FastAPI()

# Initialize Razorpay client with your API keys
razorpay_client = razorpay.Client(auth=("rzp_test_N97KSHc0rITx3P", "IRl8oZFZwOhPPhMJ5BJeRPIx"))


@app.post("/create-payment")
async def create_payment(amount: int):
    # Create a Razorpay payment order
    payment_data = {
        "amount": amount *1.00  ,# Convert amount to paisa (currency's smallest unit)
        "currency": "INR",
        "receipt": "order_receipt_1",
        "payment_capture": 1
    }

    try:
        payment = razorpay_client.order.create(data=payment_data)
        return {"payment_id": payment["id"]}
    except Exception as e:
        return {"error": str(e)}
    
    
@app.get("/verify-payment/{payment_id}")
async def verify_payment(payment_id: str):
    try:
        # Fetch the payment details from Razorpay using the payment ID
        payment = razorpay_client.payment.fetch(payment_id)
        # Check the payment status
        status = payment.get("status")
        return {"payment_status": status}
    except Exception as e:
        return {"error": str(e)}



@app.post("/razorpay-callback")
async def razorpay_callback(request: dict):
    # Verify the payment status
    payment_id = request.get("razorpay_payment_id")
    try:
        payment = razorpay_client.payment.fetch(payment_id)
        # Process the payment status (e.g., update your database)
        return {"status": payment.get("status")}
    except Exception as e:
        return {"error": str(e)}
