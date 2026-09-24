st.subheader("🚨 Anomaly Detection...")
...
model = IsolationForest(contamination=0.05, random_state=42)  <- ITHU THAAN DA!
preds = model.fit_predict(...)