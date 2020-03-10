# Contributing to py_cui

I'll welcome anyone wanting to contribute to the development of `py_cui`. If you wish to contribute to the core codebase of the library, you may want to take a look at the developers page of the [documentation](https://jwlodek.github.io/py_cui-docs/). If you have created a project that uses `py_cui`, feel free to make a pull request to add a link to your project in the `Powered by py_cui` section of the `README.md` file.


Before you create a pull request, here are some things to keep in mind:

#### Don't break backwards compatibility

In some extreme cases there may be exceptions to this, but in general I would like to retain compatibility with any previous programs written with `py_cui`. I would like to avoid a situation where projects are locked to a certain release because a new feature broke an existing one. I have already written many interfaces that I use day to day, and I would like to keep using them without dealing with multiple versions of the library. Generally, if with your changes the examples in this repository won't run without fixes, I will probably ask you to change your PR so that they do. Compatibility with older python versions is also recommended, as currently `py_cui` supports as far back as 3.2, but likely this will move to a newer version soon.

#### Make sure the unit tests pass

If you make a pull request and Travis tells you a unit test failed, please fix the issue and append to the pull request. I will most likely only look closely at pull requests that don't show any issues with the CI. Note that if your changes edit existing functions, you may need to edit the test itself to reflect them. If you are adding a new feature, please add unit tests and confirm they pass as well.

#### Use consistent numpy documentation

The documentation building process for `py_cui` depends on strict numpy-style documenatation. Please be consistent in format with the rest of the project.

#### Use the fork-pull request model

Please use the standard github fork-pull request model for contributions, preferably with creating branch names that reflect the feature or bugfix you are adding. Also, please describe what your pull request is doing when creating it, and if applicable, please add a link to any related issues or pull requests.

#### Check the AUTHORS file

If you'd like, add your name to the `Contributing Authors` section of the `AUTHORS` file. This way your name will appear in the project outside of the github environment.
