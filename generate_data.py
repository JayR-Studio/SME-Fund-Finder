import pandas as pd
import random

# Core "Seeds" for 2026 Grants
grant_types = [
    {"name": "Innovation Research Grant (SBIR)", "amount": "$150,000", "industry": "Technology"},
    {"name": "Growth Grant for Minorities", "amount": "$10,000", "industry": "General"},
    {"name": "Women-Owned Startup Fund", "amount": "$25,000", "industry": "Retail/Service"},
    {"name": "Veteran Business Support Grant", "amount": "$5,000", "industry": "Varies"},
    {"name": "Green Energy Expansion Grant", "amount": "$50,000", "industry": "Sustainability"}
]

states = ["California", "Texas", "Florida", "New York", "Pennsylvania", "Illinois", "Ohio", "Georgia", "North Carolina",
          "Michigan"]

data = []

# Generate 1,000 variations
for i in range(1000):
    seed = random.choice(grant_types)
    state = random.choice(states)

    grant_name = f"{state} {seed['name']}"
    slug = grant_name.lower().replace(" ", "-").replace("(", "").replace(")", "")

    data.append({
        "grant_name": grant_name,
        "state": state,
        "amount": seed['amount'],
        "industry": seed['industry'],
        "slug": slug,
        "deadline": "December 2026"  # 2026 updated
    })

df = pd.DataFrame(data)
df.to_csv('data/grants.csv', index=False)
print("Successfully generated 1,000 grant entries in data/grants.csv!")