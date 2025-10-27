import importlib
import inspect
from pathlib import Path

from pydantic import BaseModel


def resolve_schemas_forward_refs(apps_dir: Path | str, verbose: bool = False) -> None:
    """
    Dynamically import all Pydantic schema modules under the given 'apps' directory and rebuild them
    to resolve forward references using a shared global namespace.

    This ensures that interdependent Request/Response schemas across multiple app modules can
    correctly reference each other (e.g., circular or cross-app type hints).

    Args:
        apps_dir: Path to the root 'apps' directory. Each app submodule is expected to contain a
        'schemas' package with Pydantic models representing API request and response schemas.
        verbose: When True, enables verbose diagnostic output.

    Raises:
        FileNotFoundError: If the given 'apps' directory does not exist.
    """
    if verbose:
        print("🧩 Resolving forward references in Pydantic models...")

    apps_path = Path(apps_dir) if isinstance(apps_dir, str) else apps_dir

    if not apps_path.exists():
        raise FileNotFoundError(f"Apps directory not found: {apps_dir}")

    # STEP 1: Import all schema modules under each app
    all_modules = []

    for app_dir in apps_path.iterdir():
        if not app_dir.is_dir() or app_dir.name.startswith("_"):
            continue

        schemas_dir = app_dir / "schemas"
        if not schemas_dir.exists() or not schemas_dir.is_dir():
            continue

        for py_file in schemas_dir.glob("*.py"):
            if py_file.name.startswith("_"):
                continue

            module_name = f"apps.{app_dir.name}.schemas.{py_file.stem}"

            try:
                module = importlib.import_module(module_name)
                all_modules.append(module)
            except Exception as e:
                if verbose:
                    print(f"[WARN] Failed to import {module_name}: {e}")

    # STEP 2: Collect all BaseModel subclasses and build a shared namespace
    schemas_to_rebuild = []
    global_namespace = {}

    for schema in all_modules:
        for name, obj in inspect.getmembers(schema, inspect.isclass):
            if (
                issubclass(obj, BaseModel)
                and obj is not BaseModel
                and obj.__module__ == schema.__name__
            ):
                schemas_to_rebuild.append((name, obj))
                global_namespace[name] = obj  # Expose schema to shared namespace

    # STEP 3: Rebuild schemas using the unified namespace
    rebuilt_schemas_count = 0

    for name, schema in schemas_to_rebuild:
        try:
            schema.model_rebuild(_types_namespace=global_namespace)
            rebuilt_schemas_count += 1

            if verbose:
                print(f"Rebuilt {name}")
        except Exception as e:
            if verbose:
                print(f"[WARN] Failed to rebuild {name}: {e}")

    if verbose:
        print(
            f"🧩✅ Rebuild complete: {rebuilt_schemas_count}/{len(schemas_to_rebuild)} schemas "
            f"rebuilt successfully."
        )
