from functools import wraps

from sqlalchemy.orm import relationship as sqlalchemy_relationship


@wraps(sqlalchemy_relationship)
def safe_relationship(*args, **kwargs):
    """
    Wrapper around SQLAlchemy's `relationship()` with a default of `lazy='raise_on_sql'`.

    This helps catch accidental lazy-loading in async contexts (e.g. with FastAPI) and prevents
    silent N+1 queries during serialization or DB access.

    Override `lazy` explicitly if you want different behavior.
    """
    kwargs.setdefault("lazy", "raise_on_sql")

    return sqlalchemy_relationship(*args, **kwargs)
