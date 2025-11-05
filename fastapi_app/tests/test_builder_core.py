from fastapi_app.core.builder_core import auto_patch_function

print("=== Test auto_patch_function ===")

new_func_code = """\
def hello_world():
    print("Hello world v1.4 â€“ patched successfully!")"""

result = auto_patch_function("./fastapi_app/test_patch_target.py", "hello_world", new_func_code)
print("RÃ©sultat :", result)
