from fastapi import FastAPI


app = FastAPI(title="As Coach")


@app.get("/")
def root():
    return "Hello!"
