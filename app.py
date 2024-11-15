from decimal import Decimal
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import backend

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with a specific domain like "http://localhost:3000" in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

backend.b_init()
for i in range(8):
    backend.init_contract(10)
# Request model
class SubmitModel(BaseModel):
    walletid: str
    hf_url: str
    dataset_size: int
    client_index: int

# Response model for submit-model
class SubmitResponse(BaseModel):
    message: str
    success: bool
# Response model for get-balance
class BalanceResponse(BaseModel):
    balance: str  # Use string to handle Decimal safely

class RewardResponse(BaseModel):
    reward: int  # Use string to handle Decimal safely
# Response model for withdrawal
class WithdrawResponse(BaseModel):
    message: str
    success: bool
@app.post("/submit-model", response_model=SubmitResponse)
async def processModelSubmit(request: SubmitModel):
    try:
        print(f"Received request: {request.dict()}")

        # Simulate processing (replace with your backend logic)
        if not request.hf_url.startswith("https://huggingface.co/"):
            raise HTTPException(status_code=400, detail="Invalid Hugging Face URL.")
        if request.dataset_size <= 0:
            raise HTTPException(status_code=400, detail="Dataset size must be positive.")

        backend.update_model("wallet_id", request.client_index)
        return SubmitResponse(message="Model submitted successfully!", success=True)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")
@app.get("/withdraw", response_model=WithdrawResponse)
async def withdraw(client_index: int = Query(..., description="Index of the client")):
    try:
        # Call the backend function to withdraw rewards
        result = backend.withdraw_rewards(client_index)
        
        # Check the result
        if result == "0 Balance or withdrawal Failed":
            raise HTTPException(status_code=400, detail="Withdrawal failed: 0 balance or error.")
        
        return WithdrawResponse(message="Withdrawal successful!", success=True)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")
@app.get("/get-balance", response_model=BalanceResponse)
async def get_balance(client_index: int = Query(..., description="Index of the client")):
    try:
        balance = backend.check_current_balance(client_index)
        if isinstance(balance, Decimal):
            balance = str(balance)  # Convert Decimal to string
        return BalanceResponse(balance=balance)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")
    
@app.get("/get-reward", response_model=RewardResponse)
async def get_balance(client_index: int = Query(..., description="Index of the client")):
    try:
        reward = backend.check_reward(client_index)
        # # print(reward.dtype)
        # if isinstance(reward, int):
        #     reward = str(reward)  # Convert Decimal to string
        return RewardResponse(reward=reward)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")
