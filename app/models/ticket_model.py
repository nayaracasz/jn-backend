from pydantic import BaseModel

class EventData(BaseModel):
    eventName: str
    date: str
    zone: str
    seat: str
    price: float

class MintTicketRequest(BaseModel):
    wallet_address: str
    event_data: EventData
