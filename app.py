# --- SMART AI LOGIC - With Column Not Exist check ---
text_lower = text.lower()
answer = ""
found_col = None

# Find which column user asked about
for col in df.columns:
    if col.lower() in text_lower:
        found_col = col
        break

numeric_cols = df.select_dtypes(include=['int64','float64']).columns

# Case 1: User asked for a column that exists
if found_col:
    if found_col in numeric_cols:
        if "average" in text_lower or "mean" in text_lower:
            answer = f"Average {found_col} is {df[found_col].mean():.2f}"
        elif "sum" in text_lower or "total" in text_lower:
            answer = f"Total {found_col} is {df[found_col].sum():.2f}"
        elif "max" in text_lower or "highest" in text_lower:
            answer = f"Maximum {found_col} is {df[found_col].max()}"
        elif "min" in text_lower or "lowest" in text_lower:
            answer = f"Minimum {found_col} is {df[found_col].min()}"
        else:
            answer = f"Average {found_col} is {df[found_col].mean():.2f}"
    else:
        answer = f"Column '{found_col}' exists but it is not numeric. Cannot calculate average."

# Case 2: User asked for average/sum but column was NOT found
elif any(word in text_lower for word in ["average", "mean", "sum", "total", "max", "min", "salary", "age", "sales"]):
    # Try to extract the word after "of" -> e.g., "average of salary"
    possible_col = text_lower.split("of")[-1].strip() if "of" in text_lower else "that column"
    answer = f"Column '{possible_col}' does not exist. Available columns are: {', '.join(df.columns)}"

# Case 3: General questions
elif "how many" in text_lower or "rows" in text_lower or "count" in text_lower:
    answer = f"Total {len(df)} rows are there."
elif "column" in text_lower:
    answer = f"Columns are {', '.join(df.columns)}"
else:
    answer = f"Sorry, I could not find that column. Available columns are: {', '.join(df.columns)}"