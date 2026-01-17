# Daily Journal

## 2026-01-17 Update README

### 🎯 Goal
- Verify the startup instructions in the README.md.
- Update the file accordingly.
- Set up GitHub Actions to run tests when pushing.

### 📝 Notes
- git cloned and ran tests from scratch.
- Set up GitHub Actions and confirmed all passed except test_dummyjson.
- Refactored test_dummyjson.py by replacing jsonschema with Pydantic and confirmed all passed locally.

### Clean-up
- Deleted dummyJson_product.schema.json file as it's no longer necessary.

### 🚧 Challenges & Solutions
- **Problem**: `ModuleNotFoundError: No module named 'jsonschema'`
- **Solution**: Added Todo below instead of `uv add jsonschema` to add the missing dependency.

# Todo's
-[X] Refactor test_dummyjson_product.py by replacing jsonschema with Pydantic.
