# Football Match Prediction Application

## Description

This application predicts the outcome of football matches using four trained models. By selecting a model and inputting the home and away teams, users can forecast whether the match result will be a home win, an away win, or a draw. The four algorithms used are:

- **Gaussian Naive Bayes (GNB)**
- **Histogram-based Gradient Boosting (HGB)**
- **K-Nearest Neighbors (KNN)**
- **Random Forest (RF)**

The application leverages these models to predict match outcomes based on the chosen algorithm.

## Features

- **Model Selection**: Choose from four different prediction algorithms (**GNB**, **HGB**, **KNN**, **RF**) by clicking on the respective buttons at the top of the window.
- **Team Selection**: Select the home team from a dropdown menu. Then, select the away team from a second dropdown menu. Only matches included in the training set can be selected.
- **Prediction Results**: After selecting the teams, click the **predict** button to view the predicted match result alongside the actual historical result.
- **Feedback**: Success or error messages are displayed throughout the process, helping guide the user.
- **Testing**: A comprehensive test suite is included to systematically verify the functionality and behavior of the application.

## Usage

1. **Launch** the application.
2. **Choose an algorithm** by clicking one of the buttons (**GNB**, **HGB**, **KNN**, **RF**) at the top of the window.
3. **Select the home team** from the first dropdown menu.
4. **Select the away team** from the second dropdown menu.
5. **Click the predict button** to see the prediction result.
6. **View the predicted result** and the actual historical result.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.
