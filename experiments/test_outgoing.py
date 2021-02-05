from outgoing import check_url

def test_twitter():
    assert check_url('https://twitter.com/repsusandavis') == False
    assert check_url('https://twitter.com/edsu') == True
