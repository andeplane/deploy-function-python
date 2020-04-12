def handle(data, client, secrets):
    print("Hello anders")   
    print("Data: ", data)
    return {
        2.0 * data["value"]
    }
