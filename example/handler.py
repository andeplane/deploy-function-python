def handle(data, client, secrets):
    print("Hello anders")   
    print("Data: ", data)
    return {
        "result": 2.0 * data["value"]
    }
