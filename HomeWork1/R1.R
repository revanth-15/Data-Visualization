# Load necessary libraries
library(ggplot2)
library(dplyr)
library(tidyr)
library(corrplot)
library(readr)
library(readxl)

# Load the dataset
file_path <- "C:/Users/revan/OneDrive/Desktop/region_05.csv"

# Check if file is an Excel file or CSV
if (grepl("\\.xlsx$|\\.xls$", file_path)) {
  df <- read_excel(file_path)
} else {
  df <- tryCatch({
    read_csv(file_path)
  }, error = function(e) {
    stop("File format not recognized. Please check if it's a valid CSV or Excel file.")
  })
}

# Display basic dataset information
dataset_overview <- function(df) {
  print("Dataset Information:")
  print(str(df))
  print("\nFirst 5 Rows:")
  print(head(df))
  print("\nMissing Values:")
  print(colSums(is.na(df)))
  print("\nDuplicate Rows:")
  print(nrow(df) - nrow(unique(df)))
  print("\nDescriptive Statistics:")
  print(summary(df))
}

dataset_overview(df)

# Handling Missing Values: Drop columns with more than 50% missing values
missing_threshold <- 0.5 * nrow(df)
df_cleaned <- df %>% select(where(~ sum(is.na(.)) < missing_threshold))

# Filling remaining missing values
for (col in names(df_cleaned)) {
  if (is.character(df_cleaned[[col]])) {
    df_cleaned[[col]][is.na(df_cleaned[[col]])] <- names(sort(table(df_cleaned[[col]]), decreasing = TRUE))[1]
  } else {
    df_cleaned[[col]][is.na(df_cleaned[[col]])] <- median(df_cleaned[[col]], na.rm = TRUE)
  }
}

# Detecting and removing outliers using IQR method
remove_outliers <- function(df, column) {
  Q1 <- quantile(df[[column]], 0.25, na.rm = TRUE)
  Q3 <- quantile(df[[column]], 0.75, na.rm = TRUE)
  IQR <- Q3 - Q1
  lower_bound <- Q1 - 1.5 * IQR
  upper_bound <- Q3 + 1.5 * IQR
  df %>% filter(df[[column]] >= lower_bound & df[[column]] <= upper_bound)
}

numerical_cols <- names(df_cleaned)[sapply(df_cleaned, is.numeric)]
for (col in numerical_cols) {
  df_cleaned <- remove_outliers(df_cleaned, col)
}

# Exploratory Data Analysis (EDA) Visualizations
ggplot(df_cleaned, aes(x = iyear)) +
  geom_histogram(bins = 50, fill = "blue", alpha = 0.7) +
  labs(title = "Distribution of Events by Year", x = "Year", y = "Frequency")

# Boxplot for latitude by region
ggplot(df_cleaned, aes(x = as.factor(region), y = latitude)) +
  geom_boxplot() +
  labs(title = "Latitude Distribution by Region", x = "Region", y = "Latitude")

# Select only numeric columns for correlation analysis
numeric_df <- df_cleaned %>% select(where(is.numeric))

# Compute correlation matrix
corr_matrix <- cor(numeric_df, use = "complete.obs")

# Plot heatmap of correlation matrix
corrplot(corr_matrix, method = "color", col = colorRampPalette(c("blue", "white", "red"))(200), tl.cex = 0.8)

# Save cleaned dataset for further analysis
write_csv(df_cleaned, "C:/Users/revan/OneDrive/Desktop/cleaned_region_05.csv")
print("Cleaned dataset saved.")

