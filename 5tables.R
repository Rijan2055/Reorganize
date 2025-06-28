library(data.table)

library(tidyverse)

setwd("~/Dumpster/5tables/")

table_list <- list.files(".")

# A way to detect the empty tables
find_empty_cols <- function(dt) {
  empty_cols <- character()
  for (col in names(dt)) {
    if (all(is.na(dt[[col]]))) {
      empty_cols <- c(empty_cols, col)
    }
  }
  return(empty_cols)
}


# A function to return a subtable with 
# only the columns that are not empty.

find_non_empty_cols <- function(dt) {
  non_empty_cols <- character()
  for (col in names(dt)) {
    if (!all(is.na(dt[[col]]))) {
      non_empty_cols <- c(non_empty_cols, col)
    }
  }
  return(dt[, .SD, .SDcols = non_empty_cols])
}

# ---

arabidopsis_normal_median_values <- fread("arabidopsis_normal_median_values.csv", fill=TRUE)

arabidopsis_normal_sample_values <- fread("arabidopsis_normal_sample_values.csv", fill=TRUE)

arabidopsis_observed_median_values <- fread("arabidopsis_observed_median_values.csv", fill = TRUE)

arabidopsis_observed_sample_values <- fread("arabidopsis_observed_sample_values.csv", fill = TRUE)

arabidopsis_zscore_median_values <- fread("arabidopsis_zscore_median_values.csv", fill = TRUE)


# Some of the columns in the tables are empty and 
# require clean up.
# We will be using the find_non_emtpy_cols to drop the empty functions.


arabidopsis_normal_median_values_empty_columns_dropped <-  find_non_empty_cols(arabidopsis_normal_median_values)

arabidopsis_normal_sample_values_empty_columns_dropped <- find_non_empty_cols(arabidopsis_normal_sample_values) 

arabidopsis_observed_median_values_empty_columns_dropped <- find_non_empty_cols(arabidopsis_observed_median_values) 

arabidopsis_observed_sample_values_empty_columns_dropped <- find_non_empty_cols(arabidopsis_observed_sample_values) 

arabidopsis_zscore_median_values_empty_columns_dropped <- find_non_empty_cols(arabidopsis_zscore_median_values)

# Write these tables to file

# change dir to cleaned

setwd("cleaned/")

arabidopsis_normal_median_values_empty_columns_dropped %>% fwrite("arabidopsis_normal_median_values_empty_columns_dropped.tsv", sep =  "\t", col.names = TRUE)  

arabidopsis_normal_sample_values_empty_columns_dropped %>% fwrite("arabidopsis_normal_sample_values_empty_columns_dropped.tsv", sep =  "\t", col.names = TRUE) 

arabidopsis_observed_median_values_empty_columns_dropped %>% fwrite("arabidopsis_observed_median_values_empty_columns_dropped.tsv", sep =  "\t", col.names = TRUE) 

arabidopsis_observed_sample_values_empty_columns_dropped %>% fwrite("arabidopsis_observed_sample_values_empty_columns_dropped.tsv", sep =  "\t", col.names = TRUE) 

arabidopsis_zscore_median_values_empty_columns_dropped %>% fwrite("arabidopsis_zscore_median_values_empty_columns_dropped.tsv", sep =  "\t", col.names = TRUE) 