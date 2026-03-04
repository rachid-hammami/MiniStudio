from fastapi_app.core.builder_core import auto_repair_file

print("=== Test auto_repair_file ===")

file_to_fix = "./fastapi_app/test_patch_target.py"
result = auto_repair_file(file_to_fix)
print("RÃ©sultat rÃ©paration :", result)
