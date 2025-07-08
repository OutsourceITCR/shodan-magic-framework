from marshmallow import Schema, fields, post_dump, pre_dump, validate


class ApiResponseSchema(Schema):
    success = fields.Boolean(required=True)
    data = fields.Raw(required=False)  # Default to flexible data type
    message = fields.String(required=False, allow_none=True)
    errors = fields.List(fields.String(), required=False, missing=list, allow_none=True)

    def __init__(self, data_schema=None, many=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if data_schema:
            self.data_schema = data_schema(many=True) if many else data_schema()
            setattr(self, 'data', fields.Nested(self.data_schema, required=True))
        else:
            self.data_schema = None

    @pre_dump
    def serialize_data(self, data, **kwargs):
        """
        Expects `data` to be a dict with an optional `data` key.
        If present, `data['data']` should be either a SQLAlchemy model instance or a list of such instances.
        """
        if 'data' in data and self.data_schema:
            value = data['data']
            if isinstance(value, (list, tuple)):
                if value:
                    if all(hasattr(item, '__dict__') for item in value):
                        data['data'] = self.data_schema.dump(value)
            elif hasattr(value, '__dict__'):
                data['data'] = self.data_schema.dump(value)
        return data

    @post_dump
    def remove_null_fields(self, data, **kwargs):
        return {key: value for key, value in data.items() if value is not None}


class ApiSearchPaginationSchema(Schema):
    total = fields.Int(required=True, default=0)
    page = fields.Int(required=True, default=1)
    per_page = fields.Int(required=True, default=10)
    total_pages = fields.Int(required=True, default=1)


class APISearchOrderSchema(Schema):
    order_by = fields.Str(required=True)
    order_dir = fields.Str(required=True, validate=validate.OneOf(['asc', 'desc']))


class ApiSearchResponseSchema(ApiResponseSchema):  # Inheriting from ApiResponseSchema
    def __init__(self, records_schema=None, many=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if records_schema:
            data_schema = Schema.from_dict({
                "pagination": fields.Nested(ApiSearchPaginationSchema(), required=False),
                "order": fields.Nested(APISearchOrderSchema(), required=False),
                "records": fields.Nested(records_schema(), many=many)
            })

            setattr(self, 'data', fields.Nested(data_schema(), required=True))

            self.records_schema = records_schema(many=many)

    @pre_dump
    def serialize_records(self, data, **kwargs):
        """
        Expects `data` to be a dict with a `data` key, which itself is a dict containing a `records` key.
        `data['data']['records']` should be a SQLAlchemy model instance or a list of such instances.
        """
        if 'data' in data and 'records' in data['data']:
            records = data['data']['records']
            if isinstance(records, (list, tuple)):
                if records:
                    if all(hasattr(item, '__dict__') for item in records):
                        data['data']['records'] = self.records_schema.dump(records)
            elif hasattr(records, '__dict__'):
                data['data']['records'] = self.records_schema.dump(records)
        return data

class UserProfileSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=128),
        error_messages={"required": "Name is required.", "invalid": "Invalid name."}
    )
    email = fields.Email(
        required=True,
        error_messages={"required": "Email is required.", "invalid": "Invalid email address."}
    )
    details = fields.Dict(
        required=True,
        error_messages={"required": "Details are required.", "invalid": "Details must be a JSON object."}
    )