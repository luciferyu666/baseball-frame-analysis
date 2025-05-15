import uvicorn, os
uvicorn.run("src.api.main:app", host="0.0.0.0", port=int(os.getenv("PORT",8000)))
