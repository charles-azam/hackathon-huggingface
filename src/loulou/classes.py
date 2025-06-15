from pydantic import BaseModel, HttpUrl


class BudgetBreakdown(BaseModel):
    flights: int
    hotels: int
    activities: int
    food: int


class Flights(BaseModel):
    outbound: str
    return_: str  # 'return' is reserved in Python
    airline: str
    duration: str
    url: HttpUrl


class Hotel(BaseModel):
    name: str
    url: HttpUrl
    rating: float
    location: str
    amenities: list[str]


class Activity(BaseModel):
    name: str
    description: str
    url: HttpUrl


class Package(BaseModel):
    title: str
    duration: str
    price: int
    budgetBreakdown: BudgetBreakdown
    flights: Flights
    hotel: Hotel
    activities: list[Activity]


class Packages(BaseModel):
    packages: list[Package]
