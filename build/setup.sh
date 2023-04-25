cd data
mkdir -p fast
cd fast
wget --show-progress -O fast.nt.zip https://researchworks.oclc.org/researchdata/fast/FASTAll.nt.zip
unzip fast.nt.zip && rm fast.nt.zip
cat *.nt > fastall.nt
