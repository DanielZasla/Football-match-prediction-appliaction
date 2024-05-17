import os
import pickle
import unittest
import pandas as pd
from main import load_file


class TestSuccess(unittest.TestCase):
    """
    Please note that this test suit uses the main application to run the tests, which necessitates the closing of
    the application window manually in order to complete the tests. Once the application window is open please
    wait a moment and then close the application to ret the test results.
    """

    def load_file(self, file):
        """
        As defined per the original code from :ref:`load_file` in `main.py`. Note that the last line of code,
        `output_text.see(tk.END)`, is related to GUI and is removed for the purposes of this test.
        """
        global test_f, test_l
        temp = pd.read_csv(file)
        test_l = temp["label"]
        test_f = temp.drop("label", axis=1)

    def test_load_file(self):
        # Prepare a mock file with test data
        file = "test_file.csv"
        test_data = "label,value\nA,10\nB,20\nC,30\n"
        with open(file, "w") as f:
            f.write(test_data)

        # Call the function to be tested
        self.load_file(file)

        # Assert the expected values of test_f and test_l
        expected_test_l = pd.Series(["A", "B", "C"], name="label")
        expected_test_f = pd.DataFrame({"value": [10, 20, 30]})
        pd.testing.assert_series_equal(test_l, expected_test_l)
        pd.testing.assert_frame_equal(test_f, expected_test_f)

        # Cleanup the mock file
        os.remove(file)

    def test_loadModel(self):
        """
        Attempts to load models, thus checking both the existence of the .sav files and their respective loading of
        models.
        """
        with open('KNN.sav', 'rb') as mod:
            model = pickle.load(mod)
            name = str(type(model)).split(".")[-1][:-2]
            self.assertEqual("KNeighborsClassifier", name)
        with open('GNB.sav', 'rb') as mod:
            model = pickle.load(mod)
            name = str(type(model)).split(".")[-1][:-2]
            self.assertEqual("GaussianNB", name)
        with open('RF.sav', 'rb') as mod:
            model = pickle.load(mod)
            name = str(type(model)).split(".")[-1][:-2]
            self.assertEqual("RandomForestClassifier", name)
        with open('HGB.sav', 'rb') as mod:
            model = pickle.load(mod)
            name = str(type(model)).split(".")[-1][:-2]
            self.assertEqual("HistGradientBoostingClassifier", name)


class TestFail(unittest.TestCase):

    def test_wrongFormat(self):
        """
        Attempts to give an invalid file to the program and expects an exception.
        """
        mock_file_path = os.path.join(os.path.dirname(__file__), "main.py")
        self.assertRaises(Exception, load_file, mock_file_path, "Expected exception.")


if __name__ == '__main__':
    unittest.main()
