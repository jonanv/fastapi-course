from pydantic import BaseModel, ConfigDict, Field

class Tag(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=30,
        description="Nombre de la etiquetas",
        examples=["Esta es mi primer etiqueta"]
    )
    
    model_config = ConfigDict(from_attributes=True)