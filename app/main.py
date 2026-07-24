from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.routes import auth, student, parent
from app.api.routes import driver, route, route_stop, bus

app = FastAPI(title="School Transport Pro API")

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(parent.router)
app.include_router(driver.router)
app.include_router(route.router)
app.include_router(route_stop.router)
app.include_router(bus.router)

@app.get("/")
def read_root():
    return {"message": "School Transport Pro API running"}

@app.get("/health-check")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "success", "database": "connected"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}