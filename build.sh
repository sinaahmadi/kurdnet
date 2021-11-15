#!/bin/bash

VERSION="1.0"
DTD="WN-LMF-1.1.dtd"

# 
mkdir -p etc
if [ ! -d etc/cili ]; then
    echo "Retrieving ILI map"
    git clone https://github.com/globalwordnet/cili.git etc/cili
fi

if [ ! -d etc/omw-data ]; then
    echo "Retrieving omw-data"
    git clone https://github.com/omwn/omw-data.git etc/omw-data
fi

if [ ! -f etc/"${DTD}" ]; then
    echo "Retrieving DTD"
    wget "https://globalwordnet.github.io/schemas/${DTD}" -O etc/"$DTD"
fi

citation=$( sed -r -e '/^$/d' -e 's/\s+$//' ckb/citation.rst )

NAME="kurdnet-${VERSION}"
DIR="$NAME"

echo "Preparing package directory"
mkdir -p "$DIR"
cp README.md "$DIR"
cp LICENSE "$DIR"
cp ckb/citation.bib "$DIR"

echo "Building wordnet"
DESTINATION="${DIR}/${NAME}.xml"
PYTHONPATH=etc/omw-data python3 -m scripts.tsv2lmf \
	  ckb/wn-data-ckb.tab \
	  "$DESTINATION" \
	  --id='kurdnet' \
	  --label='KurdNet (Kurdish WordNet)' \
	  --language='ckb' \
	  --version="$VERSION" \
	  --email='ahmadi.sina@outlook.com' \
	  --license='https://creativecommons.org/licenses/by-sa/4.0/' \
	  --url="https://github.com/sinaahmadi/kurdnet" \
	  --citation="${citation}" \
	  --requires=omw-en:1.4 \
	  --ili-map=etc/cili/ili-map-pwn30.tab \
	  --log=build.log

# ensure the xml is valid
echo "Validating"
xmlstarlet val -d etc/"$DTD" "$DESTINATION"

# archive the package
echo "Archiving the package"
tar -c -J -f "${NAME}.tar.xz" "$DIR"
