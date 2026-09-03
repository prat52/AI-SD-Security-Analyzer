import json

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.architecture import Architecture
from app.models.user import User
from app.schemas.architecture_schema import ArchitectureCreate, ArchitectureResponse
from app.auth.jwt_handler import decode_token
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.services.llm_service import analyze_architecture_with_llm


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == payload["sub"]).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# @router.post("/architecture", response_model=ArchitectureResponse)
# def create_architecture(
#     arch: ArchitectureCreate,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     new_arch = Architecture(
#         content=arch.content,
#         user_id=current_user.id
#     )

#     db.add(new_arch)
#     db.commit()
#     db.refresh(new_arch)

#     return new_arch

# @router.post("/architecture", response_model=ArchitectureResponse)
# def create_architecture(
#     arch: ArchitectureCreate,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     # Call LLM
#     llm_response = analyze_architecture_with_llm(arch.content)
#     print("LLM Response:", llm_response)  # Debugging statement to check the LLM response

#       # Convert dict to JSON string for storage

#     # Save to DB
#     new_arch = Architecture(
#         content=arch.content,
#         response=llm_response,
#         user_id=current_user.id
#     )

#     db.add(new_arch)
#     db.commit()
#     db.refresh(new_arch)

#     return new_arch

@router.post("/architecture", response_model=ArchitectureResponse)
def create_architecture(
    arch: ArchitectureCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Call LLM
    llm_response = analyze_architecture_with_llm(arch.content)
    print("LLM Response:", llm_response)

    # Parse if string, keep if already dict
    if isinstance(llm_response, str):
        parsed_response = json.loads(llm_response)
    else:
        parsed_response = llm_response

    # Save raw string to DB
    new_arch = Architecture(
        content=arch.content,
        response=json.dumps(parsed_response),  # store as clean JSON string
        user_idk=current_user.id
    )

    db.add(new_arch)
    db.commit()
    db.refresh(new_arch)

    # Return parsed findings directly instead of the DB object
    return {
        "id": new_arch.id,
        "content": new_arch.content,
        "response": parsed_response,   # ← dict, not string
        "created_at": new_arch.created_at
    }



@router.get("/architectures", response_model=list[ArchitectureResponse])
def get_architectures(
    current_user: User = Depends(get_current_user)
):
    return current_user.architectures
