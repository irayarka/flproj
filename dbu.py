from models import Session, user_table, car_table, order_table


def list_users(email=None, username=None):
    session = Session()
    filters = []
    if email:
        filters.append(user_table.email.like(email))
    if username:
        filters.append(user_table.username.like(username))
    return session.query(user_table).filter(*filters).all()


def list_cars(*filters):
    session = Session()
    return session.query(order_table).join(car_table).fiter_by(*filters).all()


def get_car_by_id(model_class, carId, **kwargs):
    session = Session()
    return session.query(model_class).filter_by(carId=carId, **kwargs).one()


def create_entry(model_class, *, commit=True, **kwargs):
    session = Session()
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    return entry


def get_entry_by_username(model_class, username, **kwargs):
    session = Session()
    return session.query(model_class).filter_by(username=username, **kwargs).one()


def get_entry_by_id(model_class, id, **kwargs):
    session = Session()
    return session.query(model_class).filter_by(id=id, **kwargs).all()


def update_entry(entry, *, commit=True, **kwargs):
    session = Session()
    for key, value in kwargs.items():
        setattr(entry, key, value)
    if commit:
        session.commit()
    return entry


def delete_user(user_table, username, commit=True, **kwargs):
    session = Session()
    session.query(user_table).filter_by(username=username, **kwargs).delete()
    if commit:
        session.commit()


def delete_entry(model_class, id, *, commit=True, **kwargs):
    session = Session()
    session.query(model_class).filter_by(id=id, **kwargs).delete()
    if commit:
        session.commit()
