## Exploration Report

1 File
10 columns
8.225.871 rows

### Columns data types

| col_name | data type |
|----------|-----------------|
|country_or_area|object|
|year|int64|
|comm_code|object|
|commodity|object|
|flow|object|
|trade_usd|int64|
|weight_kg|float64|
|quantity_name|object|
|quantity|float64|
|category|object|

### Column unique values

| col_name | unique_vals |
|----------|-----------------|
|country_or_area|209|
|year|29|
|comm_code|5047|
|commodity|5031|
|flow|4|
|trade_usd|3062165|
|weight_kg|2137907|
|quantity_name|12|
|quantity|2124833|
|category|98|

### Missing values

| col_name | missing_count |
|----------|-----------------|
|country_or_area|0|
|year|0|
|comm_code|0|
|commodity|0|
|flow|0|
|trade_usd|0|
|weight_kg|128475|
|quantity_name|0|
|quantity|304857|
|category|0|

### Numeric values ranges

* year:         29 different values      from:    1988  to 2,016
* trade_usd:    3062165 different values from:    1     to 2,443,310,524,064
* weight_kg:    2137908 different values from:    0.0   to 1,860,133,241,000
* quantity:     2124834 different values from:    0.0   to 1,026,356,999,296,000

## STRING VALUES and UNIQUES

* countries has 209 unique entries
* comm_code has 5047 unique entries
* commodities has 5031 unique entries

## Up do 200 instances of string values

### STRING: flow has 4 entries
```
['Export' 'Import' 'Re-Export' 'Re-Import']
```

### STRING: quantity_name has 12 entries
```
['Number of items' 'No Quantity' 'Weight in kilograms' 'Volume in litres'
 'Length in metres' 'Area in square metres'
 'Electrical energy in thousands of kilowatt-hours'
 'Volume in cubic meters' 'Number of pairs' 'Thousands of items'
 'Weight in carats' 'Number of packages']
```

### STRING: category has 98 entries

```
['01_live_animals' '02_meat_and_edible_meat_offal'
 '03_fish_crustaceans_molluscs_aquatic_invertebrates_ne'
 '04_dairy_products_eggs_honey_edible_animal_product_nes'
 '05_products_of_animal_origin_nes'
 '06_live_trees_plants_bulbs_roots_cut_flowers_etc'
 '07_edible_vegetables_and_certain_roots_and_tubers'
 '08_edible_fruit_nuts_peel_of_citrus_fruit_melons'
 '09_coffee_tea_mate_and_spices' '10_cereals'
 '11_milling_products_malt_starches_inulin_wheat_glute'
 '12_oil_seed_oleagic_fruits_grain_seed_fruit_etc_ne'
 '13_lac_gums_resins_vegetable_saps_and_extracts_nes'
 '14_vegetable_plaiting_materials_vegetable_products_nes'
 '15_animal_vegetable_fats_and_oils_cleavage_products_et'
 '16_meat_fish_and_seafood_food_preparations_nes'
 '17_sugars_and_sugar_confectionery' '18_cocoa_and_cocoa_preparations'
 '19_cereal_flour_starch_milk_preparations_and_products'
 '20_vegetable_fruit_nut_etc_food_preparations'
 '21_miscellaneous_edible_preparations' '22_beverages_spirits_and_vinegar'
 '23_residues_wastes_of_food_industry_animal_fodder'
 '24_tobacco_and_manufactured_tobacco_substitutes'
 '25_salt_sulphur_earth_stone_plaster_lime_and_cement'
 '26_ores_slag_and_ash' '27_mineral_fuels_oils_distillation_products_etc'
 '28_inorganic_chemicals_precious_metal_compound_isotope'
 '29_organic_chemicals' '30_pharmaceutical_products' '31_fertilizers'
 '32_tanning_dyeing_extracts_tannins_derivs_pigments_et'
 '33_essential_oils_perfumes_cosmetics_toileteries'
 '34_soaps_lubricants_waxes_candles_modelling_pastes'
 '35_albuminoids_modified_starches_glues_enzymes'
 '36_explosives_pyrotechnics_matches_pyrophorics_etc'
 '37_photographic_or_cinematographic_goods'
 '38_miscellaneous_chemical_products' '39_plastics_and_articles_thereof'
 '40_rubber_and_articles_thereof'
 '41_raw_hides_and_skins_other_than_furskins_and_leather'
 '42_articles_of_leather_animal_gut_harness_travel_good'
 '43_furskins_and_artificial_fur_manufactures_thereof'
 '44_wood_and_articles_of_wood_wood_charcoal'
 '45_cork_and_articles_of_cork'
 '46_manufactures_of_plaiting_material_basketwork_etc'
 '47_pulp_of_wood_fibrous_cellulosic_material_waste_etc'
 '48_paper_paperboard_articles_of_pulp_paper_and_board'
 '49_printed_books_newspapers_pictures_etc' '50_silk'
 '51_wool_animal_hair_horsehair_yarn_and_fabric_thereof' '52_cotton'
 '53_vegetable_textile_fibres_nes_paper_yarn_woven_fabri'
 '54_manmade_filaments' '55_manmade_staple_fibres'
 '56_wadding_felt_nonwovens_yarns_twine_cordage_etc'
 '57_carpets_and_other_textile_floor_coverings'
 '58_special_woven_or_tufted_fabric_lace_tapestry_etc'
 '59_impregnated_coated_or_laminated_textile_fabric'
 '60_knitted_or_crocheted_fabric'
 '61_articles_of_apparel_accessories_knit_or_crochet'
 '62_articles_of_apparel_accessories_not_knit_or_crochet'
 '63_other_made_textile_articles_sets_worn_clothing_etc'
 '64_footwear_gaiters_and_the_like_parts_thereof'
 '65_headgear_and_parts_thereof'
 '66_umbrellas_walking_sticks_seat_sticks_whips_etc'
 '67_bird_skin_feathers_artificial_flowers_human_hair'
 '68_stone_plaster_cement_asbestos_mica_etc_articles'
 '69_ceramic_products' '70_glass_and_glassware'
 '71_pearls_precious_stones_metals_coins_etc' '72_iron_and_steel'
 '73_articles_of_iron_or_steel' '74_copper_and_articles_thereof'
 '75_nickel_and_articles_thereof' '76_aluminium_and_articles_thereof'
 '78_lead_and_articles_thereof' '79_zinc_and_articles_thereof'
 '80_tin_and_articles_thereof'
 '81_other_base_metals_cermets_articles_thereof'
 '82_tools_implements_cutlery_etc_of_base_metal'
 '83_miscellaneous_articles_of_base_metal'
 '84_nuclear_reactors_boilers_machinery_etc'
 '85_electrical_electronic_equipment'
 '86_railway_tramway_locomotives_rolling_stock_equipmen'
 '87_vehicles_other_than_railway_tramway'
 '88_aircraft_spacecraft_and_parts_thereof'
 '89_ships_boats_and_other_floating_structures'
 '90_optical_photo_technical_medical_etc_apparatus'
 '91_clocks_and_watches_and_parts_thereof'
 '92_musical_instruments_parts_and_accessories'
 '93_arms_and_ammunition_parts_and_accessories_thereof'
 '94_furniture_lighting_signs_prefabricated_buildings'
 '95_toys_games_sports_requisites'
 '96_miscellaneous_manufactured_articles'
 '97_works_of_art_collectors_pieces_and_antiques'
 '99_commodities_not_specified_according_to_kind' 'all_commodities']
```