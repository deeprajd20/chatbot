from src.config_llm import ElementAI

a = ElementAI()
while True:
    get_input = input("Enter Your Question:")
    res = a.get_response(str(get_input))
    print(res)