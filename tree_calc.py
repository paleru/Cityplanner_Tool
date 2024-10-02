import dataframe_helper as dh

def calc_trees(combined_cities_df, final_tree_info_df, predicted_df, input_year, input_value):

    combined_cities_new_df = combined_cities_df.drop(columns=['Region', 'Population', 'Waste And Sewage', 'Machinery', 'Electricity And District Heating', 'Other Heating', 'Agriculture', 'Transportation', 'Industry', 'Average Yearly Net Tree Emissions(For Whole Region)', 'Num of Cities in Region'])
    final_tree_info_new_df = final_tree_info_df.drop(columns=['Species', 'Type', 'Description', 'Average Height', 'Habitat', 'Light', 'Soil', 'Water'])

    combined_cities_new_df['City With Special Characters'] = combined_cities_new_df['City'].apply(dh.reverse_special_chars_finish)
    filtered_cities_data = combined_cities_new_df[combined_cities_new_df['Year'] >= 2022][['City With Special Characters','Total Emissions']]
    filtered_cities_data = filtered_cities_data[filtered_cities_data['City With Special Characters'].str.contains(input_value, case=False)]
    #total_2022 = filtered_cities_data['Total Emissions'].iloc[0]

    input_value = dh.replace_special_chars(input_value)
    input = input_value.capitalize()
    emissions = predicted_df[input]
    emissions_flux_subtracted = combined_cities_df[combined_cities_df['City'] == input]

    year_totals = {
        '2022': emissions[10],
        '2023': emissions[11],
        '2024': emissions[12],
        '2025': emissions[13]  
    }

    if input_year in year_totals:
        year_total = year_totals[input_year]
        offset_to_sub = emissions_flux_subtracted[emissions_flux_subtracted['Year'] == 2022]
        offset_to_sub = offset_to_sub['Average Yearly Net Tree Emissions'].values[0]
        year_total_with_offset = year_total + offset_to_sub
        print(f'Average Yearly Net Tree Emissions: {offset_to_sub}')
        print(f'year total with offset: {year_total_with_offset}')
        print(f'year total: {year_total}')

    def calc_year(total, total_with_offset):
        LARCH_CONSUMPTION = final_tree_info_new_df.loc[final_tree_info_new_df['Tree'] == 'Larch', 'Average CO2 Consumption'].iloc[0]
        larch_calc = int(total / LARCH_CONSUMPTION)
        larch_net_calc = int(total_with_offset / LARCH_CONSUMPTION)

        PINE_CONSUMPTION = final_tree_info_new_df.loc[final_tree_info_new_df['Tree'] == 'Pine', 'Average CO2 Consumption'].iloc[0]
        pine_calc = int(total / PINE_CONSUMPTION)
        pine_net_calc = int(total_with_offset / PINE_CONSUMPTION)

        DOUGLAS_CONSUMPTION = final_tree_info_new_df.loc[final_tree_info_new_df['Tree'] == 'Douglas Fir', 'Average CO2 Consumption'].iloc[0]
        douglas_calc = int(total / DOUGLAS_CONSUMPTION)
        douglas_net_calc = int(total_with_offset / DOUGLAS_CONSUMPTION)

        FIR_CONSUMPTION = final_tree_info_new_df.loc[final_tree_info_new_df['Tree'] == 'Fir', 'Average CO2 Consumption'].iloc[0]
        fir_calc = int(total / FIR_CONSUMPTION)
        fir_net_calc = int(total_with_offset / FIR_CONSUMPTION)

        SPRUCE_CONSUMPTION = final_tree_info_new_df.loc[final_tree_info_new_df['Tree'] == 'Spruce', 'Average CO2 Consumption'].iloc[0]
        spruce_calc = int(total / SPRUCE_CONSUMPTION)
        spruce_net_calc = int(total_with_offset / SPRUCE_CONSUMPTION)

        OAK_CONSUMPTION = final_tree_info_new_df.loc[final_tree_info_new_df['Tree'] == 'Oak', 'Average CO2 Consumption'].iloc[0]
        oak_calc = int(total / OAK_CONSUMPTION)
        oak_net_calc = int(total_with_offset / OAK_CONSUMPTION)

        BEECH_CONSUMPTION = final_tree_info_new_df.loc[final_tree_info_new_df['Tree'] == 'Beech', 'Average CO2 Consumption'].iloc[0]
        beech_calc = int(total / BEECH_CONSUMPTION)
        beech_net_calc = int(total_with_offset / BEECH_CONSUMPTION)

        calcs = [larch_calc, pine_calc, douglas_calc, fir_calc, spruce_calc, oak_calc, beech_calc]
        net_calcs = [larch_net_calc, pine_net_calc, douglas_net_calc, fir_net_calc, spruce_net_calc, oak_net_calc, beech_net_calc]

        return calcs, net_calcs 
    
    filtered_rec_data = final_tree_info_new_df.copy()

    filtered_rec_data['Recommended Tree Amount'], filtered_rec_data['Recommended Tree Amount with Net Offset'] = calc_year(year_total, year_total_with_offset)

    print(filtered_rec_data)
    return filtered_rec_data
