if [[ $1 -lt 10 ]]
then
  python3 excel_to_es_json.py --no-geocode -file excel/Volume_0${1}_processed_SL_COMPLETE.xlsx
else
  python3 excel_to_es_json.py --no-geocode -file excel/Volume_${1}_processed_SL_COMPLETE.xlsx
fi 
