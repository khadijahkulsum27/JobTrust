from app import model_opinion
from test_postings import POSTINGS

print()
print("%-52s %-8s %-8s %s" % ("Posting", "Kind", "FakeProb", "Model says"))
print("-" * 90)

right = 0
for p in POSTINGS:
    d = p["data"]
    o = model_opinion(d["job_title"], d["job_description"])
    prob = o.get("fake_probability")
    label = o.get("label", "-")
    expected = "LIKELY_FAKE" if p["kind"] == "scam" else "LIKELY_GENUINE"
    if label == expected:
        right += 1
    print("%-52s %-8s %-8s %s" % (p["label"][:52], p["kind"], prob, label))

print()
print("Model agreed with the label on %d of %d ads (14 made-up examples, not an accuracy)." % (right, len(POSTINGS)))