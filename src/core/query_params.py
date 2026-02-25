from typing import Any

from pydantic import BaseModel
from sqlalchemy import Select


class CommonQueryParams(BaseModel):
    page: int = 1
    limit: int = 10
    sort: str | None = None


def apply_pagination(stmt: Select, page: int, limit: int) -> Select:
    """Standard limit/offset pagination."""
    offset = (page - 1) * limit
    return stmt.offset(offset).limit(limit)


def apply_sorting(stmt: Select, model: Any, sort_str: str | None) -> Select:
    """
    Applies column sorting. 
    Examples: 'name', '-created_at', 'age,name'
    """
    if not sort_str:
        return stmt

    for part in sort_str.split(","):
        part = part.strip()
        if not part:
            continue
        
        descending = part.startswith("-")
        field_name = part[1:] if descending else part
        
        column = getattr(model, field_name, None)
        if column is not None:
            stmt = stmt.order_by(column.desc() if descending else column.asc())
            
    return stmt


def apply_filters(
    stmt: Select, 
    model: Any, 
    filters: dict[str, Any], 
    exclude: list[str] | None = None
) -> Select:
    """
    Applies basic equality filters for any key that matches a model column.
    """
    exclude = exclude or ["page", "limit", "sort", "fields"]
    
    for key, value in filters.items():
        if key in exclude or not value:
            continue
            
        column = getattr(model, key, None)
        if column is not None:
            stmt = stmt.where(column == value)
            
    return stmt


def get_pagination_meta(total: int, page: int, limit: int) -> dict[str, Any]:
    """Standard pagination metadata helper."""
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit if total > 0 else 0
    }
