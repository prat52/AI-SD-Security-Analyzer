# from fastapi import APIRouter, HTTPException
# from app.models.schema import ArchitectureRequest
# from app.services.llm_service import analyze_architecture_with_llm
# import traceback

# router = APIRouter()

# @router.post("/analyze")
# def analyze_architecture(payload: ArchitectureRequest): #converts the incoming json into an instance of ArchitectureRequest, allowing us to access the architecture_text attribute directly in our code.
#     try:
#         result = analyze_architecture_with_llm(payload.architecture_text)
#         return result
#     except Exception as e:
#         traceback.print_exc()   
#         raise HTTPException(status_code=500, detail=str(e))
# app/api/analyze.py

from fastapi import APIRouter, HTTPException
import traceback

from app.models.schema import ArchitectureRequest
from app.agents.security_review_agent import SecurityReviewAgent

router = APIRouter()
agent = SecurityReviewAgent()

@router.post("/analyze")
def analyze_architecture(payload: ArchitectureRequest):
    try:
        result = agent.run(payload.architecture_text) #stores the result of llm_service -> task -> agent in the variable result, which is then returned as the response to the API call.
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
