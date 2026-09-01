from math import ceil
from typing import Any

from sqlalchemy import func, select


def paginated_query(self, order_by: str, direction: str, page: int, per_page: int, ModelORM: Any):
    total = self.db.scalar(
        select(func.count())
        .select_from(results.subquery())
    ) or 0
    
    if total == 0:
        return 0, []
    
    total_pages = ceil(total / per_page)
    current_page = min(page, max(1, total_pages))
    order_col = ModelORM.id if order_by == "id" else func.lower(ModelORM.name)
        
    results = results.order_by(order_col.asc() if direction == "asc" else order_col.desc())
    
    start = (current_page - 1) * per_page
    items = self.db.execute(results.limit(per_page).offset(start)).scalars().all()
    
    return total, items