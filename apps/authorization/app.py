from flask import Blueprint

authorisation = Blueprint(
    "authorisation",
    __name__,
    template_folder='templates/authorisation'
)
