from generate import get_response
import os

# Retrieve the API keys from environment variables
groq_api_key = os.getenv('GROQ_API_KEY')
tavily_api_key = os.getenv('TAVILY_API_KEY')

def test_geerate():
    responnse, lag_responnse = get_response("What is the latest research on quantum computing?",  
                                            api_key=groq_api_key, 
                                            tav_key = tavily_api_key
                                            )
    
    
    assert len(responnse) > 0, "Response should not be empty"




