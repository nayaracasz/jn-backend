from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from web3.exceptions import ContractLogicError

from app.controllers.ticket_controller import TicketContract
from app.models.ticket_model import MintTicketRequest


router = APIRouter()
contract = TicketContract()

@router.post("/tickets/mint")
async def mint_ticket(request: MintTicketRequest):
    wallet_address = request.wallet_address
    event_data = request.event_data.dict()
    try:
        tx = contract.mint_ticket(wallet_address, event_data)
        tx_json = {k: (v.hex() if isinstance(v, bytes) else str(v)) for k, v in tx.items()}
        return JSONResponse(content=tx_json)
    except ContractLogicError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))\
        
@router.get("/tickets/user/{wallet_address}")
async def get_user_tickets(wallet_address: str):
    try:
        tickets = contract.get_user_tickets(wallet_address)
        return {"tickets": tickets}
    except ContractLogicError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    