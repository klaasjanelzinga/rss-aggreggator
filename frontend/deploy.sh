
set -x
set -e

npm run-script build
sed  -i 's/main\..*\.chunk\.css/main.css/' build/index.html
mv build/static/css/main.*.chunk.css build/static/css/main.css

rm -rf ../static/build && mv build ../static