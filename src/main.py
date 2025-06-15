from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from migrations.migrations_NoSQL import migrate
from views.AuthenticationView import router_authentication

origins = ["*"]

def create_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.router.include_router(router_authentication, tags=["authentication"]) 
    return app

app = create_app()

if __name__ == "__main__":  
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8083)
    
