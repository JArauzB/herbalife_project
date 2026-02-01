### How to Run

1. Clone the repository.
```bash
git clone https://github.com/FontysVenlo/sofa-2024-herbalife-sofa
cd implementation/tests
```

2. If this is your first time running the project, create a virtual environment and install the required packages.
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```


3. Run this command to create all documents of code coverage
```bash
      python -m coverage run -m unittest discover -p "test*.py" && python -m coverage report
``` 

With these steps, we can effectively measure, analyze, and visualize code coverage in the Python project, ensuring thorough testing and higher code quality.

To generate a html file to see all the functions of CODE COVERAGE in more details use the command, this will

```bash
   python -m coverage run -m unittest discover -p "test*.py" && python -m coverage report && python -m coverage html
``` 