import pandas as pd # noqa
import matplotlib
matplotlib.use('Agg') # required for Flask to serve matplotlib images
import matplotlib.pyplot as plt # noqa

def process_data(df, input_values):
    hospital_name, bed_value, income_value = input_values

    print('Received values for function: ', hospital_name, bed_value, income_value)

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
    
    def main_barchart():

        fig, ax = plt.subplots(figsize=(10, 7))
        
        # Bar colors
        main_color = '#1f75fe'  # A modern blue
        highlight_color = '#ee204d'  # A modern orange
        
        ax.bar(df['Hospital Name'], df['Net Income'], color=main_color, alpha=0.7, label='All Hospitals') # noqa: E501
        ax.bar(output_df['Hospital Name'], output_df['Net Income'], color=highlight_color, alpha=0.9, label='Selected Hospital') # noqa: E501
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

    return output_table_formated, fig1

