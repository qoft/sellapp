pip-compile pyproject.toml
pip-sync
py -m pip install --upgrade build
py -m build
py -m pip install --upgrade twine
py -m twine upload dist/*