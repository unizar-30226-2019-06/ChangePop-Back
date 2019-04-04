##  @package user
#   Documentation for this module.
#
#   More details.

from flask import Blueprint

user = Blueprint('user', __name__)


##  Documentation for a method.
#   @brief Return the info of the user id
#   @param id The user identifier
#   @return JSON info of the user
@user.route('/user/<int:id>')
def get_info(id):

    # TODO
    return 'Devolver datos en JSON del usuario' + id


