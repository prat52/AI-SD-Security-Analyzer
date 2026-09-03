from pydantic import BaseModel
from typing import List
from typing import Dict, Any


#  Define the request and response models for the API endpoints
# defines the structure of the data that will be sent to and received from the API endpoints, ensuring type safety and data validation.
class ArchitectureRequest(BaseModel):
    architecture_text: str

# defines the structure of the response that will be sent back to the client after analyzing the architecture, including lists of components, threats, attack mappings, risks, and a summary of the overall risk assessment.
# instance of AnalysisResponse will be created and populated with the analysis results before being returned to the client in the API response.
class AnalysisResponse(BaseModel):
    findings: List[Dict[str, Any]]
#     components: list
#     stride_threats: list
#     mitre_attack_mapping: list
#     owasp_risks: list
#     attack_vectors: list
#     risk_summary: dict

