from pydantic import BaseModel, HttpUrl, Field


class BudgetBreakdown(BaseModel):
    """Breakdown of costs for different aspects of the trip."""
    flights: int = Field(description="Total cost of flights in euros")
    hotels: int = Field(description="Total cost of accommodation in euros")
    activities: int = Field(description="Total cost of planned activities in euros")
    food: int = Field(description="Estimated daily food budget per person in euros")


class Flights(BaseModel):
    """Flight information for the trip."""
    outbound: str = Field(description="Departure flight details including date and time")
    return_: str = Field(description="Return flight details including date and time")  # 'return' is reserved in Python
    airline: str = Field(description="Name of the airline company")
    duration: str = Field(description="Total flight duration (e.g., '2h 30m')")
    url: HttpUrl = Field(description="URL to book the flights")


class Hotel(BaseModel):
    """Accommodation information for the trip."""
    name: str = Field(description="Name of the hotel or accommodation")
    url: HttpUrl = Field(description="URL to book the accommodation")
    rating: float = Field(description="Hotel rating from 0 to 5 stars")
    location: str = Field(description="Location or neighborhood of the accommodation")
    amenities: list[str] = Field(description="List of available amenities (e.g., ['WiFi', 'Pool', 'Breakfast'])")


class Activity(BaseModel):
    """Activity information for the trip."""
    name: str = Field(description="Name of the activity or attraction")
    description: str = Field(description="Brief description of the activity")
    url: HttpUrl = Field(description="URL for more information or booking")


class Package(BaseModel):
    """Complete travel package with all details."""
    title: str = Field(description="Descriptive title of the package (e.g., 'Luxury Barcelona Getaway')")
    duration: str = Field(description="Total duration of the trip (e.g., '10 days')")
    price: int = Field(description="Total price of the package in euros")
    budgetBreakdown: BudgetBreakdown = Field(description="Detailed breakdown of costs")
    flights: Flights = Field(description="Flight information")
    hotel: Hotel = Field(description="Accommodation information")
    n_travelers: int = Field(description="Number of travelers this package is designed for")
    activities: list[Activity] = Field(description="List of planned activities")


class Packages(BaseModel):
    """Collection of travel packages for different budgets."""
    packages: list[Package] = Field(
        description="List of three packages: low budget, medium budget, and high budget",
        min_items=3,
        max_items=3
    )
