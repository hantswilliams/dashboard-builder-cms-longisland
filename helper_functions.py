import pandas as pd

import matplotlib
matplotlib.use('Agg') # required for Flask to serve matplotlib images
import matplotlib.pyplot as plt # noqa: E402 need to import after matplotlib.use('Agg')

# Print the matplotlib style sheets
print(plt.style.available)

# Use a stylesheet for a modern look
plt.style.use('seaborn-v0_8')

def process_data(df, input_values):
    hospital_name, bed_value, income_value = input_values

    if hospital_name and hospital_name != 'Select All':
        output_df = df[df['Hospital Name'] == hospital_name]
    else:
        output_df = df

    if bed_value and bed_value != 'Select All':
        if bed_value == 'hospitals < 100 beds':
            condition = output_df['Number of Beds'] < 100
        elif bed_value == '100 beds >= hospitals < 300 beds':
            condition = (output_df['Number of Beds'] 
                         >= 100) & (output_df['Number of Beds'] < 300)
        elif bed_value == 'hospitals >= 300 beds':
            condition = output_df['Number of Beds'] >= 300
        output_df = output_df[condition]

    if income_value and income_value != 'Select All':
        condition = output_df['Net Income'] > 0 if income_value == 'Positive' else output_df['Net Income'] < 0 # noqa: E501
        output_df = output_df[condition]


    ### create descriptive sum stats
    number_of_hospital = len(output_df)
    number_beds_sum = output_df['Number of Beds'].sum()
    total_outpatient_revenue = output_df['Outpatient Revenue'].sum()
    total_inpatient_revenue = output_df['Inpatient Revenue'].sum()
    total_medicaid_charges = output_df['Medicaid Charges'].sum()
    total_net_income = output_df['Net Income'].sum()
    median_net_income_num = df['Net Income'].median()

    ### calculate the percent of total for the selected hospital
    percent_of_total_beds = number_beds_sum / df['Number of Beds'].sum()
    percent_of_total_outpatient_revenue = total_outpatient_revenue / df['Outpatient Revenue'].sum() # noqa: E501
    percent_of_total_inpatient_revenue = total_inpatient_revenue / df['Inpatient Revenue'].sum() # noqa: E501
    percent_of_total_medicaid_charges = total_medicaid_charges / df['Medicaid Charges'].sum() # noqa: E501
    percent_of_total_net_income = total_net_income / df['Net Income'].sum()
    percent_of_total_hospitals = number_of_hospital / len(df)

    ### create a new dataframe with the sum stats
    sum_stats = {
                'Percent of Total Beds': percent_of_total_beds,
                'Percent of Total Outpatient Revenue': percent_of_total_outpatient_revenue, # noqa: E501
                'Percent of Total Inpatient Revenue': percent_of_total_inpatient_revenue, # noqa: E501
                'Percent of Total Medicaid Charges': percent_of_total_medicaid_charges, # noqa: E501
                'Percent of Total Net Income': percent_of_total_net_income,
                'Percent of Total Hospitals': percent_of_total_hospitals,
                }
    
    sum_stats_df = pd.DataFrame(sum_stats, index=[0])
    
    def main_barchart():

        fig, ax = plt.subplots(figsize=(10, 7))
        
        # Bar colors
        main_color = '#1f75fe'  # A modern blue
        highlight_color = '#ee204d'  # A modern orange
        
        ax.bar(df['Hospital Name'], df['Net Income'], color=main_color, alpha=0.7, label='All Hospitals') # noqa: E501
        ax.bar(output_df['Hospital Name'], output_df['Net Income'], color=highlight_color, alpha=0.9, label='Selected Hospital') # noqa: E501
        ax.axhline(y=median_net_income_num, color='green', linestyle='--', label=f'Median: ${(median_net_income_num).round(2):,}') # noqa: E501
        ax.axhline(y=df['Net Income'].mean(), color='red', linestyle='--', label=f'Mean: ${(df["Net Income"].mean()).round(2):,}') # noqa: E501
        
        # Adjust the spines (borders)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Fonts and rotations for labels
        ax.set_xticklabels(df['Hospital Name'], rotation=70, ha='right', fontsize=10)
        ax.set_title('Hospital Net Income in 2019', fontsize=16, fontweight='bold', pad=20) # noqa: E501
        ax.set_xlabel('Hospital Name', fontsize=14, labelpad=15)
        ax.set_ylabel('Net Income', fontsize=14, labelpad=15)

        # Set the y-axis scale to be in millions
        ax.set_yticklabels(['${:,.0f} million'.format(x) for x in ax.get_yticks()/1000000]) # noqa: E501

        # add in standard deviation to the plot
        ax.axhspan(df['Net Income'].mean() - df['Net Income'].std(), df['Net Income'].mean() + df['Net Income'].std(), alpha=0.2, color='yellow', label='Standard Deviation') # noqa: E501

        # add standard deviation to the legend
        ax.legend(frameon=True, loc='upper right')
        
        fig.tight_layout()
        return fig

    fig1 = main_barchart()
    
    output_table_formated = output_df.copy()
    columns_to_format = ['Net Income', 'Number of Beds', 
                         'Outpatient Revenue', 'Inpatient Revenue', 
                         'Medicaid Charges']
    for column in columns_to_format:
        output_table_formated[column] = output_table_formated[column].apply(lambda x: "{:,}".format(x).split('.')[0]) # noqa: E501

    return output_table_formated, sum_stats_df, fig1
