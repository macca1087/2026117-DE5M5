import unittest
import pipeline
import pandas as pd
from unittest.mock import patch


class TestPipeline(unittest.TestCase):
     # ARRANGE, ACT and ASSERT <- General template
    def test_format_columns(self):
            
            df = pd.DataFrame(columns= ["Book checkout", "Customer ID"])
            result = pipeline.format_columns(df)
            self.assertEqual(list(result.columns), ["book_checkout",'customer_id'], "incorrect col names")

    
    def test_drop_missing_rows(self):
            
            df = pd.DataFrame({"name":["A",None],  "id":[1,2]})
            result = pipeline.drop_missing_rows(df)
            self.assertEqual(len(result),1,"incorrect row count")
            self.assertEqual(result.iloc[0]["name"],"A", "incorrect data")

    def test_remove_quotes(self):
            
            df = pd.DataFrame({"date": ['" 20/02/2023 "']})
            result = pipeline.remove_quotes(df, "date")
            self.assertEqual(result.loc[0, "date"], "20/02/2023","incorrect date")


    def test_parse_date_column(self):
                
            df = pd.DataFrame({"date": ["20/02/2023", "not a date"]})
            result = pipeline.parse_date_column(df, "date")
            self.assertEqual(result.loc[0, "date"], pd.Timestamp("2023-02-20"), "incorrect date")
            self.assertTrue(pd.isna(result.loc[1, "date"]), "is not null")


    def test_convert_to_int(self):
            
            df = pd.DataFrame({"id": [1.0, pd.NA]})
            result = pipeline.convert_to_int(df, "id")
            self.assertEqual(str(result["id"].dtype), "Int64", "incorrect data type")
            self.assertEqual(result.loc[0, "id"], 1,  "incorrect value")
            self.assertTrue(pd.isna(result.loc[1, "id"]), "incorrect value")

    def test_calculate_days_borrowed(self):
                
                df = pd.DataFrame({
                    "checkout": pd.to_datetime(["20/02/2023", "25/02/2023"], dayfirst=True),
                    "returned": pd.to_datetime(["25/02/2023", "24/02/2023"], dayfirst=True),
                })

                result = pipeline.calculate_days_borrowed(
                    df,
                    returned_column="returned",
                    checkout_column="checkout",)

                self.assertEqual(result.tolist(), [5, -1], "incorrect value")


    def test_save_outputs(self):

            df = pd.DataFrame({"id": [1]})
            with (
                patch.object(pd.DataFrame, "to_csv") as mock_to_csv,
                patch("pipeline.write_to_sql") as mock_write,
                ):
                    pipeline.save_outputs(df, "cleaned.csv", "customers")

            mock_to_csv.assert_called_once_with("cleaned.csv", index=False)       
            mock_write.assert_called_once_with(df, "customers")
                                                                                                                

if __name__ == "__main__":
    unittest.main()