import warnings
warnings.filterwarnings('ignore')
from airflow.hooks.postgres_hook import PostgresHook
from sql_queries import update_temperature_country_labels_query, copy_temperature_country_labels_query, update_commodites_country_labels_query


def translate_country_labels():
    postgres = PostgresHook(postgres_conn_id='postgres', schema='world')

    translation_temperature_countries = {
        # translates temperature country labels
        # previous                          : new
        'Antigua And Barbuda'               : 'Antigua and Barbuda',
        'Bosnia And Herzegovina'            : 'Bosnia and Herzegovina',
        "Côte D''Ivoire"                    : "Côte d''Ivoire",
        'Federated States Of Micronesia'    : 'Federated States of Micronesia',
        'Guinea Bissau'                     : 'Guinea-Bissau',
        'Burma'                             : 'Myanmar',
        'Reunion'                           : 'Réunion',
        'Saint Kitts And Nevis'             : 'Saint Kitts and Nevis',
        'Saint Vincent And The Grenadines'  : 'Saint Vincent and the Grenadines',
        'Sao Tome And Principe'             : 'Sao Tome and Principe',
        'Timor Leste'                       : 'Timor-Leste',
        'Trinidad And Tobago'               : 'Trinidad and Tobago',
        'Turks And Caicas Islands'          : 'Turks and Caicos Islands',
        'United States'                     : 'USA',
        # further:
        'Falkland Islands (Islas Malvinas)'         : 'Falkland Islands',
        'South Georgia And The South Sandwich Isla' : 'South Georgia and the South Sandwich Islands',
        'Isle Of Man'                               : 'Isle of Man',
        'French Southern And Antarctic Lands'       : 'French Southern and Antarctic Lands',
        'Saint Pierre And Miquelon'                 : 'Saint Pierre and Miquelon',
        'Congo (Democratic Republic Of The)'        : 'Congo',
        'Heard Island And Mcdonald Islands'         : 'Heard Island and Mcdonald Islands',
        'Bonaire, Saint Eustatius And Saba'         : 'Bonaire, Saint Eustatius and Saba',
        'Svalbard And Jan Mayen'                    : 'Svalbard and Jan Mayen',
    }

    copy_temp = {
      # 'copied to new'                 : 'existing'
        'Brunei'                        : 'Malaysia',
        'Cook Islands'                  : 'French Polynesia',
        'Bermuda'                       : 'Turks and Caicos Islands',
        'Former Sudan'                  : 'Sudan',
        'Western Germany'               : 'Germany',
        'Maldives'                      : 'Sri Lanka',
        'Netherlands Antilles'          : 'Puerto Rico',
        'Serbia and Montenegro'         : 'Serbia',
        'TFYR of Macedonia'             : 'Macedonia',
        'Tuvalu'                        : 'Fiji',
        'Wallis and Futuna Islands'     : 'Fiji',
        'Vanuatu'                       : 'New Caledonia'
    }

    translation_comm = {
        # translates commodities country labels
        # previous                          : new
        'Belgium-Luxembourg'                : 'Belgium',
        'Bolivia (Plurinational State of)'  : 'Bolivia',
        'Bosnia Herzegovina'                : 'Bosnia and Herzegovina',
        'Brunei Darussalam'                 : 'Brunei',
        'Cabo Verde'                        : 'Cape Verde',
        'Cayman Isds'                       : 'Cayman Islands',
        'Central African Rep.'              : 'Central African Republic',
        'China, Hong Kong SAR'              : 'Hong Kong',
        'China, Macao SAR'                  : 'Macau',
        'Cook Isds'                         : 'Cook Islands',
        'Czech Rep.'                        : 'Czech Republic',
        'Dominican Rep.'                    : 'Dominican Republic',
        'FS Micronesia'                     : 'Federated States of Micronesia',
        'Faeroe Isds'                       : 'Faroe Islands',
        'Fmr Fed. Rep. of Germany'          : 'Western Germany',
        'Fmr Sudan'                         : 'Former Sudan',
        "Lao People''s Dem. Rep."           : 'Laos',
        'Neth. Antilles'                    : 'Netherlands Antilles',
        'Rep. of Korea'                     : 'South Korea',
        'Rep. of Moldova'                   : 'Moldova',
        'Russian Federation'                : 'Russia',
        'Solomon Isds'                      : 'Solomon Islands',
        'State of Palestine'                : 'Palestina',
        'Turks and Caicos Isds'             : 'Turks and Caicos Islands',
        'United Rep. of Tanzania'           : 'Tanzania',
        'Viet Nam'                          : 'Vietnam',
        'Wallis and Futuna Isds'            : 'Wallis and Futuna Islands'
    }


    for prev_country_label, new_country_label in translation_temperature_countries.items():
        query = update_temperature_country_labels_query % (new_country_label, prev_country_label)
        try:
            postgres.run(query)
        except:
            print("cound not execute:")
            print(query)

    for copy_mew, existing in copy_temp.items():
        query = copy_temperature_country_labels_query % (copy_mew, existing)
        try:
            postgres.run(query)
        except:
            print("cound not execute:")
            print(query)

    for prev_country_label, new_country_label in translation_comm.items():
        query = update_commodites_country_labels_query % (new_country_label, prev_country_label)
        try:
            postgres.run(query)
        except:
            print("cound not execute:")
            print(query)