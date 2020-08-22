import functools
from typing import List, Union, Optional

import typer
from rich import print
from pydantic import BaseModel
from traktor_client import errors


def output(models: Union[BaseModel, List[BaseModel]]):
    if not isinstance(models, list):
        models = [models]

    for model in models:
        print(model)


def command(app: typer.Typer, name: Optional[str] = None):
    def decorator(func):
        @app.command(name=name)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                output(func(*args, **kwargs))
            except errors.TraktorError as e:
                print(e.message)

        return wrapper

    return decorator
