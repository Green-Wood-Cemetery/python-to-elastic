if [[ $i -lt 10 ]]
then
  python3 excel_to_es_json.py --no-geocode -file excel/Volume_0${1}_processed_SL_COMPLETE.xlsx -vol ${1} > json/greenwood-volume-${1}.json
else
  python3 excel_to_es_json.py --no-geocode -file excel/Volume_${1}_processed_SL_COMPLETE.xlsx -vol ${1} > json/greenwood-volume-${1}.json
fi 
