from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from microservices_fast_api.detect_routes import register_detect_routes
from microservices_fast_api.average_images_routes import register_average_images_routes
from microservices_fast_api.dataset_images_routes import register_dataset_images_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_detect_routes(app)
register_average_images_routes(app)
register_dataset_images_routes(app)

if __name__ == "__main__":
    print("FastAPI ready")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)