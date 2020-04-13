import time

def handle(data, client):
    print("Hello anders. Will sleep a bit now...")
    time.sleep(3.0)
    print("Did sleep. Will sleep some more, but first, print another line")
    print("Here it is.")
    time.sleep(8.0)
    print("Ok, I'm done now.")
    return {
        "result": 4.0 * data["value"]
    }