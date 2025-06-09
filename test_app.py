from generate import get_response



def test_geerate():
    responnse, lag_responnse = get_response("Hello, This is just a case showig that you are fine!")
    
    
    assert len(responnse) > 0, "Response should not be empty"




