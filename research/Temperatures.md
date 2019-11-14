## Exploration Report

1 File
4 columns
577.462 rows

### Columns data types

| col_name | data type |
|----------|-----------------|
|dt|object|
|AverageTemperature|float64|
|AverageTemperatureUncertainty|float64|
|Country|object|

### Column unique values

| col_name | unique_vals |
|----------|-----------------|
|dt|3239|
|AverageTemperature|76605|
|AverageTemperatureUncertainty|8979|
|Country|243|


### Missing values

| col_name | unique_vals |
|----------|-----------------|
|dt|0|
|AverageTemperature|32651|
|AverageTemperatureUncertainty|31912|
|Country|0|

### Numeric values ranges

* AverageTemperature:               76606 different values from:    -37.658                 to 39
* AverageTemperatureUncertainty:    8980 different values from:      0.052000000000000005   to 15

### STRING VALUES and UNIQUES

* dt has 3239 unique entries
* Country has 243 unique entries

## Up do 200 instances of string values

### STRING:  dt has 3239 entries
```
['1743-11-01' '1743-12-01' '1744-01-01' '1744-02-01' '1744-03-01'
 '1744-04-01' '1744-05-01' '1744-06-01' '1744-07-01' '1744-08-01'
 '1744-09-01' '1744-10-01' '1744-11-01' '1744-12-01' '1745-01-01'
 '1745-02-01' '1745-03-01' '1745-04-01' '1745-05-01' '1745-06-01'
 '1745-07-01' '1745-08-01' '1745-09-01' '1745-10-01' '1745-11-01'
 '1745-12-01' '1746-01-01' '1746-02-01' '1746-03-01' '1746-04-01'
 '1746-05-01' '1746-06-01' '1746-07-01' '1746-08-01' '1746-09-01'
 '1746-10-01' '1746-11-01' '1746-12-01' '1747-01-01' '1747-02-01'
 '1747-03-01' '1747-04-01' '1747-05-01' '1747-06-01' '1747-07-01'
 '1747-08-01' '1747-09-01' '1747-10-01' '1747-11-01' '1747-12-01'
 '1748-01-01' '1748-02-01' '1748-03-01' '1748-04-01' '1748-05-01'
 '1748-06-01' '1748-07-01' '1748-08-01' '1748-09-01' '1748-10-01'
 '1748-11-01' '1748-12-01' '1749-01-01' '1749-02-01' '1749-03-01'
 '1749-04-01' '1749-05-01' '1749-06-01' '1749-07-01' '1749-08-01'
 '1749-09-01' '1749-10-01' '1749-11-01' '1749-12-01' '1750-01-01'
 '1750-02-01' '1750-03-01' '1750-04-01' '1750-05-01' '1750-06-01'
 '1750-07-01' '1750-08-01' '1750-09-01' '1750-10-01' '1750-11-01'
 '1750-12-01' '1751-01-01' '1751-02-01' '1751-03-01' '1751-04-01'
 '1751-05-01' '1751-06-01' '1751-07-01' '1751-08-01' '1751-09-01'
 '1751-10-01' '1751-11-01' '1751-12-01' '1752-01-01' '1752-02-01'
 '1752-03-01' '1752-04-01' '1752-05-01' '1752-06-01' '1752-07-01'
 '1752-08-01' '1752-09-01' '1752-10-01' '1752-11-01' '1752-12-01'
 '1753-01-01' '1753-02-01' '1753-03-01' '1753-04-01' '1753-05-01'
 '1753-06-01' '1753-07-01' '1753-08-01' '1753-09-01' '1753-10-01'
 '1753-11-01' '1753-12-01' '1754-01-01' '1754-02-01' '1754-03-01'
 '1754-04-01' '1754-05-01' '1754-06-01' '1754-07-01' '1754-08-01'
 '1754-09-01' '1754-10-01' '1754-11-01' '1754-12-01' '1755-01-01'
 '1755-02-01' '1755-03-01' '1755-04-01' '1755-05-01' '1755-06-01'
 '1755-07-01' '1755-08-01' '1755-09-01' '1755-10-01' '1755-11-01'
 '1755-12-01' '1756-01-01' '1756-02-01' '1756-03-01' '1756-04-01'
 '1756-05-01' '1756-06-01' '1756-07-01' '1756-08-01' '1756-09-01'
 '1756-10-01' '1756-11-01' '1756-12-01' '1757-01-01' '1757-02-01'
 '1757-03-01' '1757-04-01' '1757-05-01' '1757-06-01' '1757-07-01'
 '1757-08-01' '1757-09-01' '1757-10-01' '1757-11-01' '1757-12-01'
 '1758-01-01' '1758-02-01' '1758-03-01' '1758-04-01' '1758-05-01'
 '1758-06-01' '1758-07-01' '1758-08-01' '1758-09-01' '1758-10-01'
 '1758-11-01' '1758-12-01' '1759-01-01' '1759-02-01' '1759-03-01'
 '1759-04-01' '1759-05-01' '1759-06-01' '1759-07-01' '1759-08-01'
 '1759-09-01' '1759-10-01' '1759-11-01' '1759-12-01' '1760-01-01'
 '1760-02-01' '1760-03-01' '1760-04-01' '1760-05-01' '1760-06-01']
```

### STRING: Country has 243 entries
```
['Åland' 'Afghanistan' 'Africa' 'Albania' 'Algeria' 'American Samoa'
 'Andorra' 'Angola' 'Anguilla' 'Antarctica' 'Antigua And Barbuda'
 'Argentina' 'Armenia' 'Aruba' 'Asia' 'Australia' 'Austria' 'Azerbaijan'
 'Bahamas' 'Bahrain' 'Baker Island' 'Bangladesh' 'Barbados' 'Belarus'
 'Belgium' 'Belize' 'Benin' 'Bhutan' 'Bolivia'
 'Bonaire, Saint Eustatius And Saba' 'Bosnia And Herzegovina' 'Botswana'
 'Brazil' 'British Virgin Islands' 'Bulgaria' 'Burkina Faso' 'Burma'
 'Burundi' "Côte D'Ivoire" 'Cambodia' 'Cameroon' 'Canada' 'Cape Verde'
 'Cayman Islands' 'Central African Republic' 'Chad' 'Chile' 'China'
 'Christmas Island' 'Colombia' 'Comoros'
 'Congo (Democratic Republic Of The)' 'Congo' 'Costa Rica' 'Croatia'
 'Cuba' 'Curaçao' 'Cyprus' 'Czech Republic' 'Denmark (Europe)' 'Denmark'
 'Djibouti' 'Dominica' 'Dominican Republic' 'Ecuador' 'Egypt'
 'El Salvador' 'Equatorial Guinea' 'Eritrea' 'Estonia' 'Ethiopia' 'Europe'
 'Falkland Islands (Islas Malvinas)' 'Faroe Islands'
 'Federated States Of Micronesia' 'Fiji' 'Finland' 'France (Europe)'
 'France' 'French Guiana' 'French Polynesia'
 'French Southern And Antarctic Lands' 'Gabon' 'Gambia' 'Gaza Strip'
 'Georgia' 'Germany' 'Ghana' 'Greece' 'Greenland' 'Grenada' 'Guadeloupe'
 'Guam' 'Guatemala' 'Guernsey' 'Guinea Bissau' 'Guinea' 'Guyana' 'Haiti'
 'Heard Island And Mcdonald Islands' 'Honduras' 'Hong Kong' 'Hungary'
 'Iceland' 'India' 'Indonesia' 'Iran' 'Iraq' 'Ireland' 'Isle Of Man'
 'Israel' 'Italy' 'Jamaica' 'Japan' 'Jersey' 'Jordan' 'Kazakhstan' 'Kenya'
 'Kingman Reef' 'Kiribati' 'Kuwait' 'Kyrgyzstan' 'Laos' 'Latvia' 'Lebanon'
 'Lesotho' 'Liberia' 'Libya' 'Liechtenstein' 'Lithuania' 'Luxembourg'
 'Macau' 'Macedonia' 'Madagascar' 'Malawi' 'Malaysia' 'Mali' 'Malta'
 'Martinique' 'Mauritania' 'Mauritius' 'Mayotte' 'Mexico' 'Moldova'
 'Monaco' 'Mongolia' 'Montenegro' 'Montserrat' 'Morocco' 'Mozambique'
 'Namibia' 'Nepal' 'Netherlands (Europe)' 'Netherlands' 'New Caledonia'
 'New Zealand' 'Nicaragua' 'Niger' 'Nigeria' 'Niue' 'North America'
 'North Korea' 'Northern Mariana Islands' 'Norway' 'Oceania' 'Oman'
 'Pakistan' 'Palau' 'Palestina' 'Palmyra Atoll' 'Panama'
 'Papua New Guinea' 'Paraguay' 'Peru' 'Philippines' 'Poland' 'Portugal'
 'Puerto Rico' 'Qatar' 'Reunion' 'Romania' 'Russia' 'Rwanda'
 'Saint Barthélemy' 'Saint Kitts And Nevis' 'Saint Lucia' 'Saint Martin'
 'Saint Pierre And Miquelon' 'Saint Vincent And The Grenadines' 'Samoa'
 'San Marino' 'Sao Tome And Principe' 'Saudi Arabia' 'Senegal' 'Serbia'
 'Seychelles' 'Sierra Leone' 'Singapore' 'Sint Maarten' 'Slovakia']
```