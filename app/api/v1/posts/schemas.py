from fastapi import Form
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Annotated, Optional, List, Literal

from ..users.schemas import UserPublic
from ..categories.schemas import CategoryPublic
from ..tags.schemas import TagPublic

class PostBase(BaseModel):
    title: str
    # content: Optional[str] = "Contenido por defecto"
    content: str
    # tags: Optional[List[TagPublic]] = []
    tags: Optional[List[TagPublic]] = Field(default_factory=list)
    user: Optional[UserPublic] = None
    image_url: Optional[str] = None
    category: Optional[CategoryPublic] = None
    
    model_config = ConfigDict(from_attributes=True)
    
class PostCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Titulo del post (mínimo 3 caracteres y máximo 100)",
        examples=["Mi primer post con FastAPI"]
    )
    content: Optional[str] = Field(
        default="Contenido no disponible",
        min_length=10,
        max_length=100,
        description="Contenido del post (mínimo 10 caracteres)",
        examples=["Este es un contenido valido por que tiene 10 caracteres o más"]
    )
    # tags: List[Tag] = []
    category_id: Optional[int] = None
    tags: List[TagPublic] = Field(default_factory=list)
    # author: Optional[Author] = None
    
    
    @field_validator("title")
    @classmethod
    def not_allowed_title(cls, value: str) -> str:
        list_not_allowed = ["spam", "prueba"]
        
        for world in list_not_allowed:
            if world in value.lower():
                raise ValueError(f"El título no puede contener la palabra: { world }")
        return value
    
    @classmethod
    def as_form(
        cls, 
        title: Annotated[str, Form(min_lenght=3)],
        content: Annotated[str, Form(min_length=10)],
        category_id: Annotated[int, Form(ge=1)] = None,
        tags: Annotated[Optional[List[str]], Form()] = None
    ):
        tags_obj = (TagPublic(name=t) for t in (tags or []))
        return cls(title=title, content=content, category_id=category_id, tags=tags_obj)

class PostUpdate(BaseModel):
    title: Optional[str] = Field(
        None, 
        min_length=3,
        max_length=100
    )
    content: Optional[str] = None
    
class PostPublic(PostBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class PostSummary(BaseModel):
    id: int
    title: str
    
    model_config = ConfigDict(from_attributes=True)
    
class PaginatedPost(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
    order_by: Literal["id", "title"]
    direction: Literal["asc", "desc"]
    search: Optional[str] = None
    items: List[PostPublic]