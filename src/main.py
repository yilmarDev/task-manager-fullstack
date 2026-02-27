from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Task Manager API")

# TODO: Configure CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# TODO: Implement your API
# Consider:
# - Authentication endpoints
# - Task CRUD operations
# - Project management
# - Permission checking
# - Health check endpoint


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    # error = True
    # if error:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST, detail="Fail Getting data"
    #     )
    return {"message": "Task Manager API is working right now"}
