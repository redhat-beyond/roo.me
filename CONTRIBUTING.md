# Contributing to roo.me

Thank you for supporting roo.me and looking for ways to help. Please note that some conventions here might be a bit different than what you are used to, even if you have contributed to other open source projects before. Reading this document will help you save time and work effectively with the developers and other contributors.

## Setting up

Before contributing to roo.me, make sure you set up the development environment by downloading the following:
1. Vagrant
2. VitualBox (or any other hypervisor)

Now, a development environment will automatically be set up for you when typing `vagrant up` in the directory of the repository.


## Issues

### Bug Reports

1. Please search both open and closed issues to make sure your bug report is not a duplicate.
2. Please try to follow the bug-report template provided.



### Feature Requests

1. Please search both open and closed issues to make sure your feature request is not a duplicate.
2. Please try to follow the feature request template provided for you.



## Pull requests

### Smaller is better

Try to keep pull requests as focused as possible on a single feature/issue, big changes are significantly less likely to be accepted.

Try not to take on too much at once. As a first-time contributor, we recommend starting with small and simple PRs in order to become familiar with the codebase. Most of the work should go into discovering which three lines need to change rather than writing the code.

### We have a template

Please make sure you follow the PR template provided for you. It makes it a lot easier for the maintainers to understand the contents of the PRs.



### Follow the Code Style Guidelines

Ensure that your code follows the [PEP 8 Style guide for Python code](https://www.python.org/dev/peps/pep-0008/) before submitting a pull request.

We have also set up Flake8 to ensure that our style guides are being followed.



### Submit finished and well-tested pull requests

Please do not submit pull requests that are still a work in progress. Pull requests should be thoroughly tested and ready to merge before they are submitted.

To test your code, run `pipenv run pytest` while inside the Vagrant machine. Make sure you add your tests too.