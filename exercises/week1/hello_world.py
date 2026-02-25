text = "Hello world"
print(text)
with open("content.txt", "w") as file:
    file.write(text)