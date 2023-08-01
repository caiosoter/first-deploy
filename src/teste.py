import os

for chave, valor in os.environ.items():
    print(f"{chave} = {valor}")