import os
import json
from dotenv import load_dotenv 

load_dotenv()

class Configuration:
    """
    Class responsible for handling the configuration of services
    """

    def __init__(self) -> None:
        self.__assert_environment_variables()

    def __assert_environment_variables(self) -> None:
        """
        Verify that all the required environment variables are defined.
        """
        required_variables: dict = [
            "IBM_API_KEY",
            "IBM_AI_ENDPOINT",
            "PROJECT_ID",
            "MODEL_ID",
            "DEBUG_PRINT"
        ]
        for required_variable in required_variables:
            assert required_variable in os.environ, f"The environment variable {required_variable} is missing."

    @property
    def ibm_api_key(self) -> str:
        """
        Returns the api key for IBM_API_KEY
        """
        return os.environ["IBM_API_KEY"]
    
    @property
    def ibm_ai_api_endpoint(self) -> str:
        """
        Returns the api endpoint for IBM AI
        """
        return os.environ["IBM_AI_ENDPOINT"]

    @property
    def project_id(self) -> str:
        """
        Returns the project ID
        """
        return os.environ["PROJECT_ID"]
 
    @property
    def model_id(self) -> str:
        """
        Returns the model ID
        """
        return os.environ["MODEL_ID"]

    @property
    def debug_print(self) -> str:
        """
        Returns the debug print(true/false)
        """
        return os.environ["DEBUG_PRINT"]

