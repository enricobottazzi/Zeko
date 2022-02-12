"""REST API through API Gateway as well as lambda handlers for each method."""

import constructs
from aws_cdk import aws_apigateway


class Api(constructs.Construct):
    def __init__(
        self,
        scope: constructs.Construct,
        constuct_id: str,
        **kwargs: Any,
    ) -> None:
        """Create the API Gateway defining an API.

        Two parts:
            1. API Gateway RestAPI instance.
            2. Set of lambda functions implementing endpoint handlers.
        """

        super().__init__(scope=scope, id=self.id)

        rest_api = aws_apigateway.RestApi(
            scope=self,
            id=f"{self.id}RestApi",
            default_method_options=aws_apigateway.MethodOptions(
                authorization_type=aws_apigateway.AuthorizationType.COGNITO
            ),
        )

        # Api Resources
        badges_resource = rest_api.root.add_resource("badges")
        badge_resource = badges_resource.add_resource("{badge_id}")

        # Handler definitions
        self.mint_badges_handler = self.create_handler(
            method_name="mint_badges",
        )

    @staticmethod
    def create_handler(
        method_name: str, **kwargs: Any
    ) -> aws_lambda_python.PythonFunction:
        """Create a new handler.

        TODO: Docstring
        """
        method_id = "".join([w.capitalize() for w in s.split("_")])

        handler = aws_lambda_python.PythonFunction(
            scope=self,
            id=method_id,
            # function_name sets the name for the lambda and the cloudwatch log. This avoids long
            # autogenerated names.
            function_name=method_id,
            entry=str(entry_path),
            index=str(method_file_path),
            handler=method_name,
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            environment=environment_variables,
            timeout=core.Duration.seconds(60),
            memory_size=512,
            retry_attempts=0,
            **kwargs,
        )