from flask import request

from middleware import validate_request, build_response
from validation import CreateCurrencySchema, UpdateCurrencySchema, PaginationSchema
from service import CurrencyService
from common import app, get_pagination, camel_dict_keys_to_underscore

PREFIX = "/api/currency"


class CurrencyApi:
    currency_service = CurrencyService()

    def __init__(self):
        self.trigger_endpoints()

    def trigger_endpoints(self):
        @app.route(PREFIX, methods=["POST"])
        @validate_request(validation_schema=CreateCurrencySchema)
        def create_currency():
            data = request.json
            new_data = camel_dict_keys_to_underscore(data)

            app.logger.info(f'Creating currency of iso code {new_data["iso_code"]}')

            currency = self.currency_service.create(new_data)
            return build_response(currency, http_status=201)

        @app.route(f"{PREFIX}/<currency_id>", methods=["GET"])
        def get_currency(currency_id):
            app.logger.info(f"Get currency of id {currency_id}")

            currency = self.currency_service.get_by_id(currency_id)
            if not currency:
                return build_response({}, http_status=200)
            return build_response(currency, http_status=200)

        @app.route(PREFIX, methods=["GET"])
        @validate_request(validation_schema=PaginationSchema)
        def list_currencies():
            req_args = request.args

            page_number, page_size = get_pagination(req_args)
            ordering = req_args.get("ordering")

            app.logger.info(
                f"Listing currencies with page_number {page_number}, page_size {page_size} and ordering {ordering}"
            )

            currencies = self.currency_service.list_all(
                page_number=page_number, page_size=page_size, ordering=ordering
            )
            return build_response(currencies, http_status=200)

        @app.route(f"{PREFIX}/<currency_id>", methods=["PUT"])
        @validate_request(validation_schema=UpdateCurrencySchema)
        def update_currency(currency_id):
            data = request.get_json(silent=True)
            new_data = camel_dict_keys_to_underscore(data)

            app.logger.info(f"Updating currency of id {currency_id}")

            updated_currency = self.currency_service.update_by_id(currency_id, new_data)
            return build_response(updated_currency, http_status=200)

        @app.route(f"{PREFIX}/<currency_id>", methods=["DELETE"])
        def delete_currency(currency_id):
            app.logger.info(f"Deleting currency of id {currency_id}")

            self.currency_service.delete_by_id(currency_id)
            return build_response({}, http_status=204)


CurrencyApi()
