# Load necessary libraries
library(ggplot2)
library(dplyr)
library(tidyr)
library(corrplot)
library(readr)

# Load the dataset
file_path <- "C:/Users/revan/OneDrive/Desktop/region_05.csv"  # Ensure the file is in the working directory
df <- read_csv(file_path)

# Display basic info
str(df)
head(df)

# Check for missing values
missing_values <- colSums(is.na(df))
missing_values <- missing_values[missing_values > 0]
missing_values <- sort(missing_values, decreasing = TRUE)

# Check for duplicate rows
duplicate_count <- sum(duplicated(df))
print(paste("Duplicate Rows:", duplicate_count))

# Summary statistics for numerical columns
numerical_summary <- summary(select(df, where(is.numeric)))
print(numerical_summary)

# Remove duplicate rows
df_cleaned <- df %>% distinct()

# Drop columns that are entirely empty
empty_cols <- names(df_cleaned)[colSums(is.na(df_cleaned)) == nrow(df_cleaned)]
df_cleaned <- df_cleaned %>% select(-all_of(empty_cols))

# Handle missing values in critical columns
df_cleaned <- df_cleaned %>% drop_na(iyear, country_txt, latitude, longitude)

# Plot incidents per year
ggplot(df_cleaned, aes(x = as.factor(iyear))) +
  geom_bar(fill = "blue") +
  theme_minimal() +
  labs(title = "Yearly Trend of Incidents", x = "Year", y = "Number of Incidents") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Top 10 countries with the most incidents
top_countries <- df_cleaned %>%
  count(country_txt, sort = TRUE) %>%
  top_n(10, n)

# Plot incidents by country
ggplot(top_countries, aes(x = reorder(country_txt, -n), y = n)) +
  geom_bar(stat = "identity", fill = "red") +
  theme_minimal() +
  labs(title = "Top 10 Countries with the Most Incidents", x = "Country", y = "Number of Incidents") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Compute correlation matrix for numerical columns
numeric_cols <- select(df_cleaned, where(is.numeric))
corr_matrix <- cor(numeric_cols, use = "complete.obs")

# Plot correlation heatmap
corrplot(corr_matrix, method = "color", col = colorRampPalette(c("blue", "white", "red"))(200), tl.cex = 0.6)

# Export cleaned dataset for Excel analysis
write_csv(df_cleaned,  "C:/Users/revan/OneDrive/Desktop/cleaned_region_05.csv")
print("Cleaned dataset saved as 'cleaned_region_05.csv'.")

