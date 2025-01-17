from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import func

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .product import Product
    from .order_product_association import OrderProductAssociation


class Order(Base):
    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )
    # products: Mapped[list["Product"]] = relationship(
    #     secondary="order_product_association",
    #     back_populates="orders",
    #     # lazy="noload",
    # )

    product_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order"
    )
