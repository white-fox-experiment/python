"""
Correct way to make test file
1 Correct way to make test class with successful test functions
1 Incorrect way to make test class with what should have been successful functions
"""
class TestClass:
    def test_me(self):
        assert True
    
    def test_me2(self):
        assert True

class MyTestClass():
    def test_it(self):
        assert True
    
    def test_it2(self):
        assert True