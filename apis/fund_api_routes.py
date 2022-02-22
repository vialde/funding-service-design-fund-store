"""
Imports the API from fund_app.py and creates the routes
in it.
"""
from apis.fund_api import api
from apis.fund_api import full_fund_model
from apis.fund_api import FUNDS
from apis.fund_api import identify_fund_model
from flask_restx import Resource


@api.route("/")
class FundList(Resource):
    @api.doc("list_funds")
    @api.marshal_list_with(identify_fund_model)
    def get(self):
        """List all funds"""
        return FUNDS.get_all()


@api.route("/<identifer>")
@api.param("identifer", "The id of the fund")
@api.response(404, "Fund not found")
class Fund(Resource):
    @api.doc("get_fund")
    @api.marshal_with(full_fund_model)
    def get(self, identifer):
        """Fetch a fund given its name"""
        return FUNDS.get(identifer)