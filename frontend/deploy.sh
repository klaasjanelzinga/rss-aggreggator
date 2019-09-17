set -x
set -e

npm run-script build
cat build/index.html | sed 's/main\..*\.chunk\.css/main.css/'  > build/index2.html
mv build/index2.html build/index.html
mv build/static/css/main.*.chunk.css build/static/css/main.css

rm -rf ../static/build && mv build ../static