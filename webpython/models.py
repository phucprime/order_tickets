from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from webpython import db


class Ticket(db.Model):
    __tablename__ = "ticket"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


if __name__ == "__main__":
    db.create_all()
