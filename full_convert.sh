echo "Converting from Excel to JSON..."
for i in {01..60}
do
  if [[ $i -lt 10 ]]
  then
    echo "python3 excel_to_es_json.py --no-geocode -file excel/Volume_0${i}_processed_SL_COMPLETE.xlsx"
    python3 excel_to_es_json.py --no-geocode -file excel/Volume_0${i}_processed_SL_COMPLETE.xlsx
  else
    echo "python3 excel_to_es_json.py --no-geocode -file excel/Volume_${i}_processed_SL_COMPLETE.xlsx"
    python3 excel_to_es_json.py --no-geocode -file excel/Volume_${i}_processed_SL_COMPLETE.xlsx
  fi
done

echo "Validate Duplicates Globally..."
python3 validate_duplicates_global.py -folder json



