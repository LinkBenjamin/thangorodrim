# Contributing to Thangorodrim

## Getting involved

If you would like to participate in the creation of the game, you can!  Here are the things you might need to know about:

- Python
- Pytest
- GitHub Actions
- SonarQube

## Setting up a Dev Environment

1. Clone the repository

`git clone https://github.com/LinkBenjamin/thangorodrim.git`

2. Create a venv

```
python -m venv venv
source venv/bin/activate
```

3. Install dependencies

`pip install -r requirements.txt`

4. Run the test suite

`pytest --cov=.`
