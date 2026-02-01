## MKDocs based documentation

### How to run it?

1. If not present, create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
```bash
source .venv/bin/activate # On Windows .venv\Scripts\activate
```

3. Move to the root folder for the documentation:
```bash
cd implementation
```

4. Install the required dependencies if not already installed:
```bash
pip install -r docs/requirements.txt
```

5. Run the documentation server:
```bash
mkdocs serve
```

6. Open the browser and navigate to `http://localhost:8000/` or `http://127.0.0.1:8000/` to see the documentation.

### Adding new pages
Go to the `implementation/docs` folder and add a new markdown file.
Depending on what kind of file you want to add:
- New class: `[Class Name]([algorithm || visualization]/classes/class_name.md)`
- New resource: `[Resource Name]([algorithm || visualization]/resources/resource_name.md)`
- New test: `[Test Name]([algorithm || visualization]/test/test_name.md)`

Heading to the MKDocs configuration file, under `implementation/docs/mkdocs.yml`, to append the new file to the navigation.

To add a reference in the documentation to the class implementation use:
```markdown
::: [algorithm || visualization]/[sub-path]/[file_name]
```