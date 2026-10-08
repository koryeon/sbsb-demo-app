from fastapi import FastAPI


app = FastAPI(title="SBSB Demo App")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello from the SBSB demo customer app"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

