def handle(data, client, secrets):
    print("Hello again anders")
    print("Data: ", data)
    return {
        4.0 * data["value"]
    }