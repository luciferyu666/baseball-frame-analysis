"""src/main.py

Module‑level entry point:

    python -m src <command> [args]

If no command is provided, show help.
"""
import sys, importlib, pkg_resources

def _list_commands():
    return [
        "run_pipeline",
        "calibrate_frames",
        "validate_dataset",
        "api"  # starts uvicorn
    ]

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src <command> [args]")
        print("Commands:", ", ".join(_list_commands()))
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "api":
        # Launch FastAPI service
        import uvicorn
        uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
        return

    try:
        mod = importlib.import_module(f"cli.{cmd}")
    except ModuleNotFoundError:
        print("Unknown command:", cmd)
        sys.exit(1)

    sys.argv = [sys.argv[0]] + sys.argv[2:]
    if hasattr(mod, "main"):
        mod.main()
    else:
        print(f"Module cli.{cmd} has no main()")
        sys.exit(1)

if __name__ == "__main__":
    main()
