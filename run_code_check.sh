# shellcheck disable=SC2046
black $(git ls-files '*.py')
pylint $(git ls-files '*.py')
