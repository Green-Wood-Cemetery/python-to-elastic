  echo "python3 clean_data.py -index ${2} -file ${1}"
  python3 clean_data.py -index ${2} -file ${1}

  echo "python3 import_data.py -file ${1} -index ${2}"
  python3 import_data.py -file ${1} -index ${2}