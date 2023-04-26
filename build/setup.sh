SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR || exit
cd ..
mkdir -p data
cd data || exit

mkdir -p models

if [[ ! -d "kp-editions" ]]; then
  git clone https://github.com/TU-plogan/kp-editions
fi

if [[ ! -s "fast/fastall.nt" ]]; then
  mkdir -p fast
  cd fast || exit
  wget --show-progress -O fast.nt.zip https://researchworks.oclc.org/researchdata/fast/FASTAll.nt.zip
  unzip fast.nt.zip && rm fast.nt.zip
  cat *.nt > fastall.nt
  cd ..
fi

# TODO: virtual env / conda

# TODO: create index & compute linguistic properties
