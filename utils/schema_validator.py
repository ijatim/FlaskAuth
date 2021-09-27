from jsonschema import Draft7Validator, validators
from uuid import UUID
from enum import Enum


class ValidationInputType(Enum):
    QUERY_PARAM = 1
    URL_PARAM = 2
    BODY = 3


def init_schema_validator(app):
    sv = SchemaValidator()
    app.schema_validator = sv


class SchemaValidator:
    def __init__(self):
        custom_type_checkers = Draft7Validator.TYPE_CHECKER.redefine_many({
            "unique_identifier": lambda _, instance: self.__is_valid_uuid(instance),
        })
        self.validator = validators.extend(validator=Draft7Validator,
                                           type_checker=custom_type_checkers)
        self.schema_types = {ValidationInputType.BODY: lambda request, kw: request.get_json(force=True),
                             ValidationInputType.QUERY_PARAM: lambda request, kw: dict(request.args),
                             ValidationInputType.URL_PARAM: lambda request, kw: kw}

    @staticmethod
    def __is_valid_uuid(uuid_to_test, version=None):
        """
        Check if uuid_to_test is a valid UUID.

         Parameters
        ----------
        uuid_to_test : str
        version : {1, 2, 3, 4, None}

         Returns
        -------
        `True` if uuid_to_test is a valid UUID, otherwise `False`.

         Examples
        --------
        # >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
        True
        # >>> is_valid_uuid('c9bf9e58')
        False
        """

        try:
            uuid_obj = UUID(uuid_to_test, version=version)
        except ValueError:
            return False
        return str(uuid_obj).lower() == uuid_to_test.lower()

    def get_errors(self,  request, kw, schema, input_type):
        """
        Validate flask Request object inputs vs provided schema
        :param request: Flask Request object
        :param kw: request URL parameters
        :param schema: provided jsonschema
        :param input_type: ValidationInputType enumerator object
        :return: list of all validation errors
        """
        errors = []
        for e in self.validator(schema).iter_errors(self.schema_types[input_type](request, kw)):
            errors.append(e)

        return errors
