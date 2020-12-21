test:
	mypy -p server
	pytest tests

clean:
	find . -name *.out -or -name *.log -or -name .*.swp -or -name .*.swo -or -name .DS_Store -or -name .swp -or -name *.pyc | xargs -n 1 rm
	rm -rf .mypy_cache
	rm -rf .pytest_cache
