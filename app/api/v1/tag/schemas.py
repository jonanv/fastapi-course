from pydantic import BaseModel, ConfigDict, Field

class TagPublic(BaseModel):
    id: int
    name: str = Field(
        ...,
        min_length=3,
        max_length=30,
        description="Nombre de la etiquetas",
        examples=["Esta es mi primer etiqueta"]
    )
    
    model_config = ConfigDict(from_attributes=True) # sirve para permitir que un modelo lea datos directamente de los atributos de un objeto normal (como una instancia de una base de datos o un ORM como SQLAlchemy)
    
class TagCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=30,
        description="Nombre de la etiquetas",
        examples=["Esta es mi primer etiqueta"]
    )
    
class TagUpdate(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=30,
        description="Nombre de la etiquetas",
        examples=["Esta es mi primer etiqueta"]
    )
    
class TagWithCount(TagPublic):
    uses: int