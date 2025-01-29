from src import zbCitData_st

data_ = "zbRevCit.csv"
dataFr = zbCitData_st.load_csv_to_dataframe(data_)  # Load main dataset
train_, test_, valid_ = zbCitData_st.getData_de(dataFr)  # Split data into train, test, valid