rmdir /s /q dist
rmdir /s /q build
python .\setup.py bdist_wheel
twine upload -u coco56 -p password dist/*
pip install --upgrade pacc
pip install --upgrade pacc
git add .
git commit -m "������%date:~0,4%��%date:~5,2%��%date:~8,2%��	%time%"
git push -f origin main
python -m pip install --upgrade pip
pip install --upgrade pacc