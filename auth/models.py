from sqlmodel import Field, Session, SQLModel, create_engine, select


class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, title="Имя пользователя")
    email: str = Field(index=True, title="Email пользователя")
    password: str = Field(title="Пароль пользователя")
