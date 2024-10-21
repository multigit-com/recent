# This is an example repository file for testing purposes

def hello_world():
    print("Hello, World!")

class ExampleClass:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello, {self.name}!")

if __name__ == "__main__":
    hello_world()
    example = ExampleClass("Tester")
    example.greet()
