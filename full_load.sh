echo "Importing JSON into ElasticSearch..."
for i in {01..60}
do
  if [[ $i -lt 10 ]]
  then
    echo "python clean_data.py -index ${1} -file json/greenwood-volume-${i}.json"
    python3 clean_data.py -index ${1} -file json/greenwood-volume-${i}.json

    echo "python import_data.py -file json/greenwood-volume-${i}.json -index ${1}"
    python3 import_data.py -file json/greenwood-volume-${i}.json -index ${1}
  else
    echo "python clean_data.py -index ${1} -file json/greenwood-volume-${i}.json"
    python3 clean_data.py -index ${1} -file json/greenwood-volume-${i}.json

    echo "python import_data.py -file json/greenwood-volume-${i}.json -index ${1}"
    python3 import_data.py -file json/greenwood-volume-${i}.json -index ${1}
  fi

  sleep 60
done
