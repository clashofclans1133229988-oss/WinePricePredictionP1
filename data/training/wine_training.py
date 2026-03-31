# =====================================================================
# SCRIPT TO VIEW THE CONTENTS OF rf_features.pkl
# =====================================================================
# This script loads and displays the pickled feature names
# These are the feature names in the exact order the ML model expects
# =====================================================================

# Import pickle module - used to load binary/serialized files
import pickle

# =====================================================================
# LOAD THE PICKLE FILE
# =====================================================================

# Open the pickle file in READ BINARY ('rb') mode
# 'rb' = read binary (binary files are computer-compiled format)
# 'with' statement automatically closes the file when done
with open('WinePricePredictionP1/rf_features.pkl', 'rb') as f:
    # pickle.load(f) deserializes (converts) the binary file back to Python object
    # In this case, it's a list of feature names
    features = pickle.load(f)

# =====================================================================
# DISPLAY THE FEATURES
# =====================================================================

# Print a header
print("\n" + "="*70)
print("📋 LOADED FEATURES FROM rf_features.pkl")
print("="*70)

# Print the entire features list
print(f"\n✅ Features (as list):\n{features}")

# Print number of features
print(f"\n📊 Total number of features: {len(features)}")

# Print each feature with its index (position)
print("\n📑 Features with their index positions:")
print("-" * 70)
for index, feature in enumerate(features):
    # enumerate gives us both the index (0, 1, 2...) and the value
    print(f"   Index {index}: {feature}")

# Print features as a formatted table
print("\n📊 Features Summary:")
print("-" * 70)
for i, feature_name in enumerate(features, 1):
    # i starts from 1 (not 0) because humans count from 1, not 0
    print(f"   {i:2d}. {feature_name}")

# Print the data type
print(f"\n🔍 Data type of features variable: {type(features)}")
print(f"🔍 Data type of first feature: {type(features[0])}")

# Print features as a single line (compact)
print(f"\n💾 Features as single line:\n   {', '.join(features)}")

print("\n" + "="*70)
print("✅ Script completed successfully!")
print("="*70 + "\n")