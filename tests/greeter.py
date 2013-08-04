def say_hello():
    return "Hello World!"

def service_check():
    return {"status": 200, "body": "OK"}

class Greeter:
    def __init__(self, greeting):
        self.greeting = greeting
    def say_hello(self, to_whom = "World!"):
        return "%s %s" % (self.greeting, to_whom)

