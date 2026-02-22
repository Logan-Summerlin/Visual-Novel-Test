# Visual-Novel-Test

Ren'Py visual novel project: **Echoes of the Forgotten Tower**.

## Local validation (production checks)

Run all static and flow tests:

```bash
python -m unittest -v tests/test_renpy_project.py
```

Optionally validate test-module syntax:

```bash
python -m py_compile tests/test_renpy_project.py
```

Run Ren'Py lint with the SDK (8.0+):

```bash
# Example using Ren'Py 8.5.2 SDK extracted to /tmp/renpy-sdk
/tmp/renpy-sdk/renpy-8.5.2-sdk/renpy.sh /workspace/Visual-Novel-Test lint
```

The lint pass checks script/screen usage and reports content statistics. Combine
lint + unittest results before release.
