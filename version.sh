set -e

function prompt {
    echo $1
    select yn in "Yes" "No"; do
        case $yn in
            Yes ) echo "OK"; break;;
            No ) exit;;
        esac
    done
}

# upgrade version
upversion up $@

# set current version
NAME=$(python setup.py --name)
VERSION=$(python setup.py --version)

if [[ -z $VERSION ]]; then
    echo "Missing version"
    exit 1
fi

if [[ $(hg tags | grep "^${VERSION}\s") ]]; then
    echo "Already existing version. Check version number."
    exit 1
fi

echo "Version: $VERSION"

echo "Generating history"
dicto view --hg-version tip --prepend HISTORY.rst

git diff | tee
prompt "Create tag $VERSION for $NAME?"

git commit -am "Bumps version ${VERSION}"
git tag $VERSION

echo "Uploading $NAME $VERSION to pypiserver"
python setup.py sdist bdist_wheel upload -r internal
